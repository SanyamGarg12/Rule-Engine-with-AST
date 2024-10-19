from pyparsing import (
    Word, alphas, alphanums, nums, oneOf, infixNotation, opAssoc, 
    quotedString, removeQuotes, ParserElement
)
from dataclasses import asdict, dataclass
# import json
import re

# Enable packrat parsing for better performance
ParserElement.enablePackrat()
@dataclass
class Node:
    def __init__(self, node_type, value, left=None, right=None):
        self.node_type = node_type
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node({self.node_type}, {self.value}, {self.left}, {self.right})"

    def to_dict(self):
        node_dict = {
            "type": self.node_type,
            "value": self.value
        }
        if self.left:
            node_dict["left"] = self.left.to_dict()
        if self.right:
            node_dict["right"] = self.right.to_dict()
        return node_dict
    
    def get_type(self):
        return self.node_type
    
def parse_rule(rule_string: str) -> dict:
    rule_string = rule_string
    # Define grammar
    identifier = Word(alphas, alphanums + "_")
    integer = Word(nums)
    real = Word(nums + ".")
    comparison_op = oneOf("> >= < <= == = != ")
    and_op = oneOf("AND and")
    or_op = oneOf("OR or")
    string = quotedString.setParseAction(removeQuotes)
    
    operand = (identifier("field") + comparison_op("operator") + (real | integer | string)("value"))
    
    expr = infixNotation(
        operand,
        [
            (and_op, 2, opAssoc.LEFT),
            (or_op, 2, opAssoc.LEFT),
        ],
    )

    parsed = tokenize_rule(rule_string)
    print(parsed)
    ast = parse_tokens(parsed)
    return ast

def tokenize_rule(rule_string):
    rule_string = '(' + rule_string + ')'
    pattern = r"(\bAND\b|\bOR\b|\(|\)|[><=!]=?|'.*?'|\w+)"
    tokens = re.findall(pattern, rule_string)
    return tokens

# Helper function to create the AST from tokens
def parse_tokens(tokens):
    def parse_expression(index):
        if index >= len(tokens):
            raise SyntaxError("Unexpected end of input")
        
        if tokens[index] == '(':
            left_node, next_index = parse_expression(index + 1)
            if next_index >= len(tokens) or tokens[next_index] not in ['AND', 'OR']:
                raise SyntaxError("Expected logical operator (AND/OR) after sub-expression")
            operator = tokens[next_index]  # AND/OR
            right_node, next_index = parse_expression(next_index + 1)
            if next_index >= len(tokens) or tokens[next_index] != ')':
                raise SyntaxError("Expected closing parenthesis")
            return Node('operator', operator, left_node, right_node), next_index + 1
        else:
            if index + 2 >= len(tokens):
                raise SyntaxError("Incomplete condition")
            condition = {
                "field": tokens[index],
                "operator": tokens[index + 1],
                "value": tokens[index + 2].strip("'")
            }
            return Node('operand', condition), index + 3
    
    ast_root, _ = parse_expression(0)
    return ast_root.to_dict()

def convert_value(val):
    # Try to convert the value into an int, float, or string based on content
    try:
        if isinstance(val, str):
            if '.' in val:
                return float(val)
            else:
                return int(val)
        return val
    except ValueError:
        return val  # Return as string if conversion fails

def combine_asts(asts: list) -> dict:
    # Combine multiple ASTs with AND logic
    if not asts:
        return {}

    combined_ast = asts[0]
    for ast in asts[1:]:
        combined_ast = {
            "type": "operator",
            "operator": "AND",
            "left": combined_ast,
            "right": ast
        }
    return combined_ast

import json
def evaluate_ast(ast: dict, data: dict) -> bool:
    if "type" not in ast:
        raise ValueError("AST is missing the 'type' key.")
    
    node_type = ast["type"]

    if node_type == "operator":
        operator = 0
        if "value" in ast:
            operator = ast["value"]
        else:
            operator = ast["operator"]  

        # Check that left and right keys are present
        if "left" not in ast or "right" not in ast:
            raise ValueError("Operator node must have 'left' and 'right' children.")
        
        left = evaluate_ast(ast["left"], data)
        right = evaluate_ast(ast["right"], data)
        
        # Evaluate based on the logical operator (AND/OR)
        if operator == "AND":
            return left and right
        elif operator == "OR":
            return left or right
        else:
            raise ValueError(f"Unknown operator: {operator}")
    
    # Process "operand" node
    elif node_type == "operand":
        if "value" not in ast:
            raise ValueError("Operand node is missing the 'value' key.")
        
        condition = ast["value"]
        field = condition["field"]
        operator = condition["operator"]
        value = convert_value(condition["value"])
        user_value = convert_value(data.get(field))

        if user_value is None:
            return False

        if isinstance(user_value, str):
            user_value = user_value.lower()
            value = value.lower() if isinstance(value, str) else value
       
        try:
            if operator == ">":
                return user_value > value
            elif operator == ">=":
                return user_value >= value
            elif operator == "<":
                return user_value < value
            elif operator == "<=":
                return user_value <= value
            elif operator in ["==", "="]:
                return user_value == value
            elif operator == "!=":
                return user_value != value
            else:
                raise ValueError(f"Unsupported operator: {operator}")
        except TypeError:
            return False  # Incomparable types
    else:
        raise ValueError(f"Unknown node type: {node_type}")

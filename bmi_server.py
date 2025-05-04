"""
BMI Calculator Server
This script implements an MCP server that provides BMI calculation functionality.
It exposes a tool that accepts weight and height parameters and returns the BMI value.
"""

from mcp.server.fastmcp import FastMCP

# Initialize the MCP server with name and version
mcp = FastMCP("BMI Calculator")

print("Starting server...", mcp.name)

@mcp.tool()
def calculate_bmi(weight: float, height: float) -> float:
    """
    Calculate Body Mass Index (BMI) using weight and height.
    
    Args:
        weight (float): Weight in kilograms
        height (float): Height in meters
        
    Returns:
        float: Calculated BMI value
        
    Raises:
        ValueError: If height is zero or negative
    """
    if height <= 0:
        raise ValueError("Height must be greater than 0")
    return weight / (height ** 2)

@mcp.tool()
def get_bmi_category(bmi: float) -> str:
    """
    Determine the BMI category based on the calculated BMI value.
    
    Args:
        bmi (float): Calculated BMI value
        
    Returns:
        str: Corresponding BMI category
    """
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"


if __name__ == "__main__":
    # Start the server using stdio transport
    mcp.run(transport="stdio")
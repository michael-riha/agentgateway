from mcp.server.fastmcp import FastMCP

def setup_system_prompts(mcp: FastMCP):
    """Setup system prompts as mentioned in the article"""
    
    @mcp.prompt()
    def get_system_prompt() -> str:
        """Get the system prompt for AI assistance"""
        return """You are a helpful assistant with access to calculator tools 
        and personalized greetings. You can perform mathematical operations 
        and provide friendly greetings to users."""
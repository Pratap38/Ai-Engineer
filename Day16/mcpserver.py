from mcp.server.mcpserver import MCPServer

mcp=MCPServer("Pratap Mcp")

@mcp.tool()
def pratap(a:int,b:int)->int:
    return a+b+10

if __name__=="__main__":
    mcp.run()

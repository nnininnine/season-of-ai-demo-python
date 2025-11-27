from project_mcp.mcp import mcp
import logging
import project_mcp.mcp_tools  # Ensure tools are registered


def main():
    logging.info("Initialize server")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

"""
Simple chant example using MCPAgent with built-in conversation memory.
Uses Groq API and MCPClient to create an interactive CLI agent.
"""

import json
import os
from pathlib import Path
from typing import Optional
from mcp_use import MCPAgent, MCPClient


from langchain_groq import ChatGroq
# Update this import based on your actual MCP module name
# from mcp_use import MCPClient


class MCPAgentDemo:
    """
    A simple MCP Agent with conversation memory.
    Demonstrates how to:
    - Load config from Browser_mcp.json
    - Initialize Groq LLM
    - Create an MCP client
    - Run an interactive agent with memory
    """

    def __init__(
        self,
        config_path: str = "Browser_mcp.json",
        max_steps: int = 10,
        memory_enabled: bool = True,
    ):
        """
        Initialize the MCP Agent.

        Args:
            config_path: Path to the MCP configuration file
            max_steps: Maximum number of agent steps
            memory_enabled: Enable conversation memory
        """
        self.config_path = config_path
        self.max_steps = max_steps
        self.memory_enabled = memory_enabled
        self.conversation_history = []

        # Initialize components
        self.config = self._load_config()
        self.llm = self._initialize_llm()
        self.client = self._initialize_mcp_client()

    def _load_config(self) -> dict:
        """Load MCP configuration from JSON file."""
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
            print(f"✓ Configuration loaded from {self.config_path}")
            return config
        except FileNotFoundError:
            print(f"✗ Configuration file not found: {self.config_path}")
            return {}
        except json.JSONDecodeError:
            print(f"✗ Invalid JSON in {self.config_path}")
            return {}

    def _initialize_llm(self) -> ChatGroq:
        """Initialize Groq LLM with API key."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable not set. "
                "Please set it before running the agent."
            )

        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=api_key,
            temperature=0.7,
        )
        print("✓ Groq LLM initialized (llama-3.3-70b-versatile)")
        return llm

    def _initialize_mcp_client(self) -> Optional[MCPClient]:
        """Initialize MCP Client with configuration."""
        try:
            client = MCPClient(config=self.config)
            print("✓ MCP Client initialized")
            return client
        except Exception as e:
            print(f"✗ Failed to initialize MCP Client: {e}")
            return None

    def _add_to_memory(self, role: str, content: str) -> None:
        """Add message to conversation memory."""
        if self.memory_enabled:
            self.conversation_history.append({"role": role, "content": content})

    def _get_memory_context(self) -> str:
        """Get formatted conversation memory for context."""
        if not self.memory_enabled or not self.conversation_history:
            return ""

        memory_text = "\n=== Conversation History ===\n"
        for msg in self.conversation_history[-4:]:  # Keep last 4 messages
            memory_text += f"{msg['role'].upper()}: {msg['content']}\n"
        return memory_text

    def process_query(self, user_input: str) -> str:
        """
        Process user query with the agent.

        Args:
            user_input: User's input message

        Returns:
            Agent's response
        """
        # Add user message to memory
        self._add_to_memory("user", user_input)

        # Build prompt with memory context
        memory_context = self._get_memory_context()
        system_prompt = (
            "You are a helpful AI assistant. "
            "You engage in friendly conversation and can help with various tasks. "
            "Be concise and helpful."
        )

        if memory_context:
            system_prompt += f"\n\n{memory_context}"

        try:
            # Get response from LLM
            response = self.llm.invoke(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ]
            )
            assistant_response = response.content

            # Add assistant response to memory
            self._add_to_memory("assistant", assistant_response)

            return assistant_response

        except Exception as e:
            error_msg = f"Error processing query: {e}"
            self._add_to_memory("assistant", f"Error: {error_msg}")
            return error_msg

    def run_cli(self) -> None:
        """Run the agent in interactive CLI mode."""
        print("\n" + "=" * 60)
        print("MCP Agent with Conversation Memory - CLI Interface")
        print("=" * 60)
        print(f"Max Steps: {self.max_steps}")
        print(f"Memory Enabled: {self.memory_enabled}")
        print("Type 'exit' to quit, 'history' to see memory, 'clear' to reset\n")

        step_count = 0

        while step_count < self.max_steps:
            try:
                # Get user input
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                # Handle special commands
                if user_input.lower() == "exit":
                    print("\nGoodbye! Thanks for chatting.")
                    break

                if user_input.lower() == "history":
                    if self.conversation_history:
                        print("\n=== Conversation Memory ===")
                        for msg in self.conversation_history:
                            print(f"{msg['role'].upper()}: {msg['content'][:100]}...")
                        print()
                    else:
                        print("\nNo conversation history yet.\n")
                    continue

                if user_input.lower() == "clear":
                    self.conversation_history = []
                    print("\n✓ Memory cleared\n")
                    continue

                # Process the query
                response = self.process_query(user_input)
                print(f"\nAgent: {response}\n")

                step_count += 1

            except KeyboardInterrupt:
                print("\n\nInterrupted by user.")
                break
            except Exception as e:
                print(f"\nError: {e}\n")

        print("\n" + "=" * 60)
        print(f"Session ended. Total steps: {step_count}")
        print("=" * 60)


def main():
    """Main entry point."""
    try:
        # Create agent with memory enabled
        agent = MCPAgentDemo(
            config_path="Browser_mcp.json",
            max_steps=10,
            memory_enabled=True,
        )

        # Run in CLI mode
        agent.run_cli()

    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease set GROQ_API_KEY environment variable:")
        print("  Windows (PowerShell): $env:GROQ_API_KEY='your-api-key'")
        print("  Windows (CMD): set GROQ_API_KEY=your-api-key")
        print("  Linux/Mac: export GROQ_API_KEY='your-api-key'")
    except Exception as e:
        print(f"Fatal Error: {e}")


if __name__ == "__main__":
    main()

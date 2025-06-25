To-Do List
 - [ ] Use crawl4ai to crawl with url input
 - [X] Build API
 - [X] Support Human Feedback Loop
 - [X] Add Deploy + API Text2Speech
 - [ ] Research UI
 - [ ] Write Detail Readme.md
 - [ ] Podcast Generation
 - [ ] Powerpoint Generation
 - [ ] Host + Support Voice as Input


 ## 1. Test Generate Podcard
 ```python
 from src.podcast.graph.builder import build_graph
 workflow = build_graph()
 report_content = """"
# Anthropic Model Context Protocol (MCP) Report

## Key Points

*   Anthropic's Model Context Protocol (MCP) is an open standard introduced in late November 2024, designed to standardize how AI models interact with external data and tools.
*   MCP acts as a universal interface, similar to a "USB port," facilitating easier integration of AI models with various data sources and services without custom integrations.
"""
final_state = workflow.invoke({"input": report_content})

with open("final.wav", "wb") as f:
        f.write(final_state["output"])
 ```

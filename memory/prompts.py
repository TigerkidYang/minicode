SUMMARY_PROMPT = """
You should write a concise summary of the given conversation logs 
between an AI coding agent and its user. 
The summary should focus on the technical details of what was accomplished, 
what files were created or modified, 
what bugs were fixed, 
and what the current ongoing goal is. 
Ignore any polite chat or exact code blocks in the logs.

This is the format you should use for the summary:

```
## Goal

[What goal(s) is the user trying to accomplish?]

## Instructions

- [What important instructions did the user give you that are relevant]
- [If there is a plan or spec, include information about it so next agent can continue using it]

## Discoveries

[What notable things were learned during this conversation that would be useful for the next agent to know when continuing the work]

## Accomplished

[What work has been completed, what work is still in progress, and what work is left?]

## Relevant files / directories

[Construct a structured list of relevant files that have been read, edited, or created that pertain to the task at hand. If all the files in a directory are relevant, include the path to the directory.]
```
"""
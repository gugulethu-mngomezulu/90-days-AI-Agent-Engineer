import json

from llm_client import MOCK_MODE, client, MODEL
from tools import calculate_skill_match, TOOL_DEFINITION


def run_agent(
    resume_skills: list[str],
    required_skills: list[str],
) -> str:

    print("\n[WEEK 6] Starting agent loop...")

    if MOCK_MODE:
        print("[MOCK MODE] Simulating LLM tool selection.")

        messages = [
            {
                "role": "user",
                "content": "Compare resume skills with job requirements.",
            }
        ]

        # Simulated tool request from an LLM
        simulated_tool_call = {
            "name": "calculate_skill_match",
            "arguments": {
                "resume_skills": resume_skills,
                "required_skills": required_skills,
            },
        }

        print("\n[AGENT] Iteration 1")
        print("[AGENT] Simulated tool request:")
        print(json.dumps(simulated_tool_call, indent=2))

        # Validate which tools are allowed
        allowed_tools = {
            "calculate_skill_match": calculate_skill_match,
        }

        function_name = simulated_tool_call["name"]

        if function_name not in allowed_tools:
            raise ValueError("Tool is not permitted.")

        # Execute real Python function
        tool_result = allowed_tools[function_name](
            **simulated_tool_call["arguments"]
        )

        messages.append(
            {
                "role": "tool",
                "content": json.dumps(tool_result),
            }
        )

        print("\n[AGENT] Python tool executed successfully!")
        print(json.dumps(tool_result, indent=2))

        print("\n[AGENT] Iteration 2")
        print("[MOCK MODE] Simulating final LLM response.")

        return (
            f"Skill overlap: {tool_result['match_percentage']}%. "
            f"Matched skills: {', '.join(tool_result['matched_skills'])}. "
            f"Missing skills: {', '.join(tool_result['missing_skills'])}. "
            "This percentage represents simple keyword overlap, "
            "not a hiring or ATS score."
        )

    # Real LLM mode
    messages = [
        {
            "role": "system",
            "content": (
                "You are a resume skill comparison agent. "
                "You must use calculate_skill_match. "
                "Never invent a percentage."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Resume skills: {json.dumps(resume_skills)}\n"
                f"Required skills: {json.dumps(required_skills)}"
            ),
        },
    ]

    allowed_tools = {
        "calculate_skill_match": calculate_skill_match
    }

    tool_was_called = False

    for iteration in range(3):

        print(f"\n[AGENT] Iteration {iteration + 1}")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=[TOOL_DEFINITION],
            tool_choice="required" if not tool_was_called else "none",
            temperature=0,
        )

        message = response.choices[0].message

        if not message.tool_calls:
            if not tool_was_called:
                raise RuntimeError("Agent did not execute a tool.")
            return message.content or "No final response."

        messages.append(message.model_dump(exclude_none=True))

        for tool_call in message.tool_calls:

            name = tool_call.function.name

            if name not in allowed_tools:
                result = {"error": "Tool not permitted"}
            else:
                try:
                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                    if arguments != {
                        "resume_skills": resume_skills,
                        "required_skills": required_skills,
                    }:
                        raise ValueError("Unexpected tool arguments")

                    result = allowed_tools[name](**arguments)

                except (ValueError, TypeError, KeyError) as error:
                    result = {"error": str(error)}

            print("[AGENT] Tool result:")
            print(json.dumps(result, indent=2))

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

            tool_was_called = True

    raise RuntimeError("Maximum agent iterations reached.")
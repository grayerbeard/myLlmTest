from openai import OpenAI, types
from pathlib import Path

# type simplification
ChatCompletionMessage = types.chat.chat_completion_message.ChatCompletionMessage
ChatHistoryEntry = ChatCompletionMessage | dict[str, str]

# Globals
requestOptions = {}


def getRequestOptions() -> dict:
    """
    Generate the request options by asking the user (unless we already asked)

    Returns:
        dict: DESCRIPTION.

    """
    global requestOptions

    if requestOptions == {}:
        print("please enter options that we will pass on with each request to the LLM (all are optional)")
        requestOptions['model'] = inputStringOrDefault("ID of the model to use:", "local-model")

        frequency_penalty = inputFloatBetween("frequency_penalty: Number between -2.0 and 2.0", min_value=-2.0, max_value=2.0, allow_null=True)
        if frequency_penalty is not None:
            requestOptions['frequency_penalty'] = frequency_penalty

        max_tokens = inputInt("max_tokens: The maximum number of [tokens](/tokenizer) that can be generated in the chat completion", True)
        if max_tokens is not None:
            requestOptions['max_tokens'] = max_tokens

        presence_penalty = inputFloatBetween("presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.", min_value=-2.0, max_value=2.0, allow_null=True)
        if presence_penalty is not None:
            requestOptions['presence_penalty'] = presence_penalty

        temperature = inputFloatBetween("temperature: What sampling temperature to use, between 0 and 2.0. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.", min_value=0.0, max_value=2.0, allow_null=True)
        if temperature is not None:
            requestOptions['temperature'] = temperature
    return requestOptions


def getAnswer(api: OpenAI, messages: list[ChatHistoryEntry]) -> ChatCompletionMessage:
    """
    Send a message to the OpenAI API and retrieve the corresponding answer.

    This function formats the input message, sends it to the OpenAI API, and
    retrieves the response. Both the message and the response are appended to
    the global `messageHistory`. The function ensures that both input and output
    messages are stripped of leading and trailing whitespace.

    Args:
        api (openai.OpenAI): An instance of the OpenAI API client.
        message (str): The message string to send to the OpenAI API.

    Returns:
        str: The content of the answer received from the OpenAI API, stripped of
        leading and trailing whitespace.

    Global Variables:
        messageHistory (List[Dict[str, str]]): A list of message dictionaries maintaining
        the history of interactions. Each dictionary has 'role' and 'content' as keys.
    """
    # Send the message to the API and get the response.
    completion = api.chat.completions.create(
        **getRequestOptions(),
        messages=messages
    )

    # add the answer to the history and return it
    answer = completion.choices[0].message
    return answer


def getMessageHistoryEntry(content: str | ChatCompletionMessage, role: str = 'user') -> ChatHistoryEntry:
    """
    Convert the input to an Entry for the Messagehistory.

    Args:
        content (str | ChatCompletionMessage): the content of the message or a ChatCompletionMessage.
        role (str, optional): the role to use for the message if the content is not a ChatCompletionMessage. Defaults to 'user'.

    Returns:
        ChatHistoryEntry: an Entry that can be addede to the message history.

    """
    if isinstance(content, ChatCompletionMessage):
        return content
    else:
        return {'role': str(role), 'content': str(content)}


def fillOutputFileUsingConversationHistory(api: OpenAI, system_message: str | None, inputFile: Path, outputFile: Path) -> None:
    """
    Run the Test while providing the complete history as a chatlog

    Args:
        api (OpenAI): the OpenAi API Object.
        system_message (str | None): the System Message.
        inputFile (Path): the File the Test should be read from.
        outputFile (Path): the file the result should be written to.

    Returns:
        None.

    """
    messages = []
    if system_message:
        messages.append(getMessageHistoryEntry(content=system_message, role='system'))
    with inputFile.open('r', encoding='UTF-8') as inputFile:
        with outputFile.open('w', encoding='UTF-8') as outputFile:
            for line in inputFile:
                if line.startswith('- Q: '):
                    outputFile.write(line)
                    line = line[5:].strip()
                    print("generating answer for:", line)
                    messages.append(getMessageHistoryEntry(content=line))  # appending current line to message log
                    answer = getAnswer(api, messages)  # generating response to the question
                    messages.append(answer)  # appending the answer to the message log
                    outputFile.write('- A: ' + answer.content.strip() + '\n')
                elif line.startswith('- A:'):
                    pass
                else:
                    outputFile.write(line)


def main() -> None:
    """Execute the Main Program"""
    # get connection details
    api_key = inputStringOrNull("please enter the API key (leave empty to load from environment variables): ")
    base_url = inputStringOrNull("please enter the baseUrl (leave empty to load from environment variables or to use OpenAI): ")
    outputFile = Path(inputStringOrDefault("what should the name (and path) of the result file be? ", "LLM TestResult.md"))
    inputFile = Path(inputStringOrDefault("what is the name (and path) of the test file? ", "LLM Test.md"))
    system_message = inputStringOrNull("what should the System message be (empty for none)? ")
    getRequestOptions()

    outputFile.parent.mkdir(parents=True, exist_ok=True)
    api = OpenAI(base_url=base_url, api_key=api_key)

    fillOutputFileUsingConversationHistory(api, system_message, inputFile, outputFile)


# Helper functions:
def inputFloatBetween(question: str, min_value: float, max_value: float, allow_null: bool = False) -> float | None:
    """
    Get a float between min_value and max_value from the user

    Args:
        question (str): the prompt the user is presented with.
        min_value (float)
        max_value (float)
        allow_null (bool, optional): weather we should return None when the input is empty. Defaults to False.

    Returns:
        float or None: only returns None if allow_null is true.

    """
    while True:
        try:
            result = input(question.strip() + " ")
            if not result.strip() and allow_null:
                return None
            else:
                result = float(result)
            if result > max_value or result < min_value:
                print(f"please enter a float between {min_value} and {max_value}")
            else:
                return result
        except Exception:
            print(f"please enter a float between {min_value} and {max_value}")


def inputInt(question: str, allow_null: bool = False) -> int | None:
    """
    Get an int from the user

    Args:
        question (str): the prompt the user is presented with.
        allow_null (bool, optional): weather we should return None when the input is empty. Defaults to False.

    Returns:
        float or None: only returns None if allow_null is true.

    """
    while True:
        try:
            result = input(question.strip() + " ")
            if not result.strip() and allow_null:
                return None
            else:
                return int(result)
        except Exception:
            print("please enter an integer (whole number)")


def inputStringOrNull(question: str) -> str | None:
    """
    Ask the user for a String, returns null if the input was empty

    Args:
        question (str): the prompt the user is presented with.

    Returns:
        result (TYPE): the stripped user input or null if empty.

    """
    result = input(question.strip() + " ").strip()
    if not result:
        return None
    else:
        return result


def inputStringOrDefault(question: str, default: str) -> str:
    """
    Ask the user for a String, returns the default if the input was empty

    Args:
        question (str): the prompt the user is presented with.
        default (str): the default value if the respunse from the user was empty.

    Returns:
        str: DESCRIPTION.

    """
    result = inputStringOrNull(question=question)
    if not result:
        return default
    else:
        return result


# executing main
if __name__ == '__main__':
    main()

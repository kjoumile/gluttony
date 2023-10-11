import os
import torch
import random
from peft import (
    PeftConfig,
    PeftModel,
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)

os.environ["cpu"] = "0"

# путь до папки с adapter_config и adapter_model
PEFT_MODEL = "generation_conf/"

config = PeftConfig.from_pretrained(PEFT_MODEL)
model = AutoModelForCausalLM.from_pretrained(
    config.base_model_name_or_path,
    return_dict=True,
    device_map="cpu",
    trust_remote_code=True
)

tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)
tokenizer.pad_token = tokenizer.eos_token

model = PeftModel.from_pretrained(model, PEFT_MODEL)
model.to(device='cpu')
import re

# костыли фиксят вывод
def remove_duplicate_phrase(input_string):

    words = re.findall(r'\b\w+\b', input_string)
    unique_phrases = set()
    filtered_words = []
    for word in words:

        if word.lower() in unique_phrases:
            continue
        else:

            unique_phrases.add(word.lower())
            filtered_words.append(word)


    result = ' '.join(filtered_words)
    return result



def remove_h_a(input_string):
  start_string = '<human>:'
  end_string = '<assistant>:'

  start_index = input_string.find(start_string)
  end_index = input_string.find(end_string) + len(end_string)

  if start_index != -1 and end_index != -1:
      output_string = input_string[:start_index] + input_string[end_index:]
  else:
      output_string = input_string
  return output_string


def add_delete_word(input_string, bank):
    words = bank.split()  # Банк слов для рандомизации вывода


    operation = random.choice(['add', 'delete', 'pass'])

    if operation == 'add':

        new_word = random.choice(words)


        updated_words = words.copy()
        updated_words.append(new_word)


        output_string = ' '.join(updated_words)
    if operation == 'delete':
        if len(words) > 1:

            index = random.randint(0, len(words) - 1)


            updated_words = words.copy()
            removed_word = updated_words.pop(index)


            output_string = ' '.join(updated_words)
        else:
            output_string = input_string
    else:
        output_string = input_string

    return output_string
# доделать
def restore_url(input):
    string = str(input)
    pattern = r"(https?://\S+)"
    match = re.search(pattern, string)
    if match:

        url = match.group(1)
        print("Извлеченная ссылка:", url)

        restored_url = re.sub(r"(?<=\S)(?=\S)", " ", url)
        return input.replace(url,restored_url)
    else:
        pass



# промпт в строку <human>: <assistant>: заполнить если нужно вставить конкретные слова в вывод
def generate_text_gamling(human,assistant = ''):
    generation_config = model.generation_config
    generation_config.max_new_tokens = 20
    generation_config.num_return_sequences = 1
    generation_config.pad_token_id = tokenizer.eos_token_id
    generation_config.eos_token_id = tokenizer.eos_token_id

    device = "cpu"
    prompt = """
    <human>: """+str(human)+"""
    <assistant>: """+ assistant+"""
    """.strip()
    encoding = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.inference_mode():
        outputs = model.generate(
            input_ids=encoding.input_ids,
            attention_mask=encoding.attention_mask,
            generation_config=generation_config
        )
    output_string = remove_duplicate_phrase(remove_h_a(str(tokenizer.decode(outputs[0], skip_special_tokens=True))))
    words_to_remove = ['assistant ', 'assistant', ' assistant', ' assistant ' ]
    for word in words_to_remove:
        output_string = output_string.replace(word, "")
    return output_string + "\ntake free spins from my referral please https://betworld.cc/go/2a5f10f7bd15426b268ae4242aaa9b3e365b64d1eb0a0b0b/"
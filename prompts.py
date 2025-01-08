class Prompts:
    def __init__(self):
        self.prompts_dict = None
        self.initialize_prompt_dict()

    def initialize_prompt_dict(self):
        self.prompts_dict = {
            "analyze": open(
                r'C:\Users\אביב\Desktop\works\Chrome-Extentions\Auto-Form-Filler-ai\prompts\analyze_prompt.txt',
                'r').read(),

            "fill": open(
                r'C:\Users\אביב\Desktop\works\Chrome-Extentions\Auto-Form-Filler-ai\prompts\fill_fields_prompt.txt',
                'r').read(),
            "extract_name": open(
                r'C:\Users\אביב\Desktop\works\Chrome-Extentions\Auto-Form-Filler-ai\prompts\extract_name.txt').read()
        }

    def get_prompt(self, prompt_type):
        try:
            return self.prompts_dict[prompt_type]
        except KeyError:
            return None


prompts = Prompts()

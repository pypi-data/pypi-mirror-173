from typing import Optional
import random as rd
import time
import json

__all__ = ("Trivia",)


class Trivia:
    def __init__(self):
        self.trivia = {"questions": {}}

    async def add(
        self,
        question: str,
        answer: str,
        options: dict,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
    ) -> str:
        """
        ## Description
        --------------
        This function will add a new question with followed by the given parameters to a JSON file.
        The options argument requires a directory, ex. `{'A': 'Answer_1', 'B': 'Answer_2'}`.

        ## Short Example
        --------------

        More examples are available on our github: https://github.com/StawaDev/Estrapy-API/tree/main/Examples

        ```
        from Estrapy import Trivia

        EstraTrivia = Trivia()
        ```

        ## Arguments:
            - question: str -- The question to add
            - answer: str -- The answer of the question
            - options: dict -- The options of the question
            - category: Optional[str] -- The category of the question
            - difficulty: Optional[str] -- The difficulty of the question
        """

        num = 1
        i = 0

        with open("trivia.json", "r", encoding="utf-8") as f:
            try:
                trivia = json.load(f)
                num = max(map(int, trivia["questions"].keys())) + 1
            except:
                trivia = self.trivia

            try:
                for _ in trivia["questions"].items():
                    i += 1
                    if trivia["questions"][str(i)]["question"] == question:
                        return "Trivia: Question (#{}) is already exist on Question (#{})".format(
                            num, i
                        )
            except:
                pass

            try:
                existing = {int(key) for key in trivia["questions"]}
                missing = [i for i in range(1, max(existing)) if i not in existing]
                num = missing[0]
            except:
                pass

            trivia["questions"].update(
                (
                    {
                        num: {
                            "question": question,
                            "answer": answer,
                            "options": options,
                            "difficulty": difficulty,
                            "category": category,
                        }
                    }
                )
            )

            with open("trivia.json", "w", encoding="utf-8") as f:
                json.dump(trivia, f, indent=4, ensure_ascii=False)
                return "Question (#{}) added".format(num)

    async def remove(self, num: int) -> None:
        """
        ## Description
        --------------
        There's nothing special about this function but it does can remove specific question you want to remove from the JSON file.

        ## Short Example
        --------------

        More examples are available on our github: https://github.com/StawaDev/Estrapy-API/tree/main/Examples

        ```
        from Estrapy import Trivia

        EstraTrivia = Trivia()
        async def remove_question():
            print(await EstraTrivia.remove(1))  # Remove question number 1
        ```

        ## Arguments:
            - num: int -- The number of question to remove
        """

        with open("trivia.json", "r", encoding="utf-8") as f:
            try:
                trivia = json.load(f)
            except:
                return "Trivia: No Question Found"

        trivia["questions"].pop(str(num))
        with open("trivia.json", "w", encoding="utf-8") as f:
            json.dump(trivia, f, indent=4, ensure_ascii=False)
            return "Trivia: Question (#{}) Removed".format(num)

    async def run(self, num: Optional[int] = None, random_pick: bool = True) -> None:
        """
        ## Description
        --------------
        Play Estra Trivia using functions, recommended using this function for Discord Bot.

        ## Short Example
        --------------
        More examples are available on our github: https://github.com/StawaDev/Estrapy-API/tree/main/Examples

        ## Arguments:
            - num: Optional[int] -- Number of the question to pick
            - random_pick: bool = True -- Randomize to pick available questions
        """

        if num and random_pick is not None:
            return "Please put None on unnecessary parameter or leave it empty"

        num = 0

        with open("trivia.json", "r") as f:
            _file = json.load(f)["questions"]
            total = len(_file)

        if random_pick:
            num = rd.randint(1, total)

        while num <= int(total):
            _options = []
            questions = _file[str(num)]["question"]
            answer = _file[str(num)]["answer"]
            options = _file[str(num)]["options"]
            difficulty = _file[str(num)]["difficulty"]
            category = _file[str(num)]["category"]

            for i in options:
                _options.append("{}.{}".format(i, options[i]))

            return num, questions, answer, _options, difficulty, category

    async def answer(self, run: any, guess: str = None):
        """
        ## Description
        --------------
        Answer the question using function, this is function will be checking if the answer is correct or not.
        Recommended using `Estrapy.Trivia.run()` method.

        Examples available in https://github.com/StawaDev/Estrapy-API/blob/main/Examples/Trivia.py

        ## Arguments:
            - run: any -- Requires argument from `Estrapy.Trivia.run`
            - guess: str -- Player's guess
        """

        if str.lower(guess) == str.lower(run[2]):
            return True, run[2]
        return False, run[2]

    async def run_console(random_pick: bool = False) -> None:
        """
        ## Description
        --------------
        Play Estra Trivia only using console, easy to access and interact!

        ## Short Example
        --------------

        More examples are available on our github: https://github.com/StawaDev/Estrapy-API/tree/main/Examples

        ```
        from Estrapy import Trivia

        EstraTrivia = Trivia()

        async def console():
            await EstraTrivia.run_console()
        ```

        ## Arguments:
            - random_pick: bool = True -- Randomize to pick available questions
        """

        score = 0
        _options = []

        with open("trivia.json", "r") as f:
            File = json.load(f)
            Total = len(File["questions"])

        if random_pick:
            num = rd.randint(1, Total)

        for num in range(1, Total + 1):
            questions = File["questions"][str(num)]["question"]
            answers = File["questions"][str(num)]["answer"]
            options = File["questions"][str(num)]["options"]
            difficulty = File["questions"][str(num)]["difficulty"]
            category = File["questions"][str(num)]["category"]

            for i in options:
                _options.append("{}.{}".format(i, options[i]))

            print("Question (#{}) : {}".format(num, questions))
            print("Options: {}".format(", ".join(_options)))
            print("Difficulty: {}".format(difficulty))
            print("Category: {}".format(category))
            answer = input("Answer: ")

            if str.lower(answer) == str.lower(answers):
                score += 1

            print(
                "That's correct!"
                if str.lower(answer) == str.lower(answers)
                else "That's incorrect!"
            )
            time.sleep(2)
            for x in options:
                _options.remove("{}.{}".format(x, options[x]))
        else:
            print(
                "Game over! no more questions! Score: {}%".format(
                    int(score / Total * 100)
                )
            )

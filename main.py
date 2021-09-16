from bs4 import BeautifulSoup
import datetime
from requests_html import HTMLSession


def main(url):
    try:
        session = HTMLSession()

        r = session.get(url)
        r.html.render(sleep=10)

        text = str(r.html.html).encode("utf-8")

    except Exception as e:
        print(e)
        print(f"[!] Something wrong happened. Unable to acess TryHackMe.")
        return

    soup = BeautifulSoup(text, 'html.parser')

    try:
        tasks = {}
        for task in soup.find_all(attrs={"class": "card-link"}):
            task_name = task.text.replace('\n', '').replace('                            ', '')
            tasks.update({f"{task_name}": {"questions": []}})

        for task in tasks:
            task_numb = task.split(' ')[1]
            questions = soup.find(id=f"task-{task_numb}")
            questions_element = questions.find_all(attrs={"class": "room-task-questions"})
            for question_numb in range(len(questions_element)):
                question = questions_element[question_numb]

                if question.div is not None:
                    tasks[task]["questions"].append(
                        str(question.div.text).replace("\n                                ", "").replace("\n", ""))
                elif question.p is not None:
                    tasks[task]["questions"].append(str(question.p.text))

        with open(f"README.md", "w+") as file:
            infos = ""

            for task in tasks:
                infos += f"## {task}\n"
                for question in tasks[task]["questions"]:
                    infos += f"- {question}\n\n	- ``\n\n"

            file.write(f"#{soup.find(id='title').text}\n\n- {datetime.datetime.now().strftime('%B %d, %Y')}\n\n"
                       f"-------------------------\n\n\n{infos}")
    except Exception as e:
        print(e)
        return

    print(f"[!] File generated sucessfully!\n")
    return


if __name__ == "__main__":
    while True:
        url = input("[?] Insert the Try Hack Me URL: ")
        main(url)

from datetime import datetime
import json
import random

class Quiz:
    def __init__(self, quiz_id, question, choices, answer, hint):
        self.quiz_id = quiz_id
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def check_answer(self, user_answer):
        return user_answer == self.answer


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.high_score = 0
        self.score_history = []
        self.load_quizzes()

    def add_quiz(self, quiz):
        self.quizzes.append(quiz)

    def load_quizzes(self):
        with open("state.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            self.high_score = data.get("high_score", 0)
            self.score_history = data.get("score_history", [])

        for quiz_data in data["quizzes"]:
            quiz = Quiz(
                quiz_data["id"],
                quiz_data["question"],
                quiz_data["choices"],
                quiz_data["answer"],
                quiz_data["hint"]
            )

            self.quizzes.append(quiz)


    def save_quizzes(self):
        data = {
            "quizzes": [],
            "score_history": self.score_history,
            "high_score": self.high_score
        }

        for quiz in self.quizzes:
            quiz_data = {
                "id": quiz.quiz_id,
                "question": quiz.question,
                "choices": quiz.choices,
                "answer": quiz.answer,
                "hint": quiz.hint
            }

            data["quizzes"].append(quiz_data)

        with open("state.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    
    def create_quiz(self):
        while True:
            question = input("문제를 입력하세요: ").strip()

            if question:
                break
            else:
                print("문제는 빈칸으로 입력할 수 없습니다.")

        choices = []

        for i in range(4):
            while True:
                choice = input(f"{i + 1}번 보기: ").strip()

                if choice:
                    choices.append(choice)
                    break
                else:
                    print("보기는 빈칸으로 입력할 수 없습니다.")

        while True:
            try:
                answer = int(input("정답 번호를 입력하세요: ")) - 1

                if 0 <= answer <= 3:
                    break
                else:
                    print("1부터 4 사이의 숫자를 입력해 주세요.")

            except ValueError:
                print("숫자로 입력해 주세요.")

        while True:
            hint = input("힌트를 입력하세요: ").strip()

            if hint:
                break
            else:
                print("힌트는 빈칸으로 입력할 수 없습니다.")

        next_id = max(
            (quiz.quiz_id for quiz in self.quizzes),
            default=0
        ) + 1

        quiz = Quiz(
            next_id,
            question,
            choices,
            answer,
            hint
        )

        self.quizzes.append(quiz)

        for i, quiz in enumerate(self.quizzes, start=1):
            quiz.quiz_id = i

        self.save_quizzes()

        print("퀴즈가 추가되었습니다!")


    def show_menu(self):
        print("\n===== 치이카와 퀴즈 게임 =====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가하기")
        print("3. 퀴즈 목록 보기")
        print("4. 퀴즈 삭제하기")
        print("5. 최고 점수 보기")
        print("6. 점수 기록 보기")
        print("7. 종료하기")

        while True:
            choice = input("메뉴를 선택하세요: ")

            if choice == "1":
                self.play_quiz()
            elif choice == "2":
                self.create_quiz()
            elif choice == "3":
                self.show_quizzes()
            elif choice == "4":
                self.delete_quiz()
            elif choice == "5":
                self.show_high_score()
            elif choice == "6":
                self.show_score_history()
            elif choice == "7":
                print("게임을 종료합니다.")
                break
            else:
                print("잘못된 입력입니다.")
            
    def show_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print("\n===== 퀴즈 목록 =====")

        for quiz in self.quizzes:
            print(f"\n번호: {quiz.quiz_id}")
            print(f"문제: {quiz.question}")

            for i, choice in enumerate(quiz.choices):
                print(f"{i + 1}. {choice}")

    
    def delete_quiz(self):
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        self.show_quizzes()

        while True:
            try:
                quiz_id = int(input("삭제할 퀴즈 번호를 입력하세요: "))

                if quiz_id <= 0:
                    print("1 이상의 번호를 입력해 주세요.")
                    continue

                for quiz in self.quizzes:
                    if quiz.quiz_id == quiz_id:
                        while True:
                            confirm = input(
                                f"'{quiz.question}' 퀴즈를 삭제하시겠습니까? (y/n): "
                            ).strip().lower()

                            if confirm == "y":
                                self.quizzes.remove(quiz)

                                for i, quiz in enumerate(self.quizzes, start=1):
                                    quiz.quiz_id = i

                                self.save_quizzes()
                                print("퀴즈가 삭제되었습니다!")
                                return

                            elif confirm == "n":
                                print("퀴즈 삭제가 취소되었습니다.")
                                return

                            else:
                                print("y 또는 n으로 입력해 주세요.")

                print("존재하지 않는 퀴즈 번호입니다.")
                continue

            except ValueError:
                print("숫자로 입력해 주세요.")


    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0

        print("\n===== 퀴즈 시작! =====")

        random_quizzes = self.quizzes.copy()
        random.shuffle(random_quizzes)

        total = len(random_quizzes)

        while True:
            try:
                question_count = int(input(f"몇 문제를 풀까요? (1~{total}): "))

                if 1 <= question_count <= total:
                    break
                else:
                    print(f"1부터 {total} 사이의 숫자를 입력해 주세요.")

            except ValueError:
                print("숫자로 입력해 주세요.")

        random_quizzes = random_quizzes[:question_count]

        for quiz in random_quizzes:
            print(f"\n문제: {quiz.question}")

            hint_used = False

            while True:
                use_hint = input("힌트를 사용하시겠습니까? (y/n): ").lower()

                if use_hint == "y":
                    print(f"힌트: {quiz.hint}")
                    hint_used = True
                    break
                elif use_hint == "n":
                    break
                else:
                    print("y 또는 n으로 입력해 주세요.")

            for i, choice in enumerate(quiz.choices):
                print(f"{i + 1}. {choice}")

            while True:
                try:
                    answer = int(input("정답 번호를 입력하세요: ")) - 1

                    if 0 <= answer < len(quiz.choices):
                        break
                    else:
                        print("보기 번호 안에서 입력해 주세요.")

                except ValueError:
                    print("숫자로 입력해 주세요.")

            if quiz.check_answer(answer):
                if hint_used:
                    print("정답입니다! 하지만 힌트를 사용해서 점수는 획득하지 못했습니다.")
                else:
                    print("정답입니다!")
                    score += 1
            else:
                print("틀렸습니다.")

        print("\n===== 퀴즈 종료! =====")
        print(f"총 {question_count}문제 중 {score}문제 정답!")
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": question_count,
            "correct": score,
            "score": score
        }

        self.score_history.append(record)
        self.save_quizzes()

        if score > self.high_score:
            self.high_score = score
            self.save_quizzes()
            print("최고 점수 갱신!")

    def show_high_score(self):
        print("\n===== 최고 점수 =====")
        print(f"최고 점수: {self.high_score}점")

    def show_score_history(self):
        if not self.score_history:
            print("아직 점수 기록이 없습니다.")
            return

        print("\n===== 점수 기록 =====")

        for record in self.score_history:
            print(f"\n날짜: {record['date']}")
            print(f"전체 문제: {record['total']}개")
            print(f"정답: {record['correct']}개")
            print(f"점수: {record['score']}점")
        

game = QuizGame()
game.show_menu()
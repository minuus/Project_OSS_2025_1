from budget import Budget


def main():
    budget = Budget()

    while True:
        print("\n==== 간단 가계부 ====")
        print("1. 지출 추가")
        print("2. 지출 목록 보기")
        print("3. 총 지출 보기")
        print("4. 데이터 백업")
        print("5. 데이터 복원")
        print("6. 백업 목록 보기")
        print("7. 종료")
        choice = input("선택 > ")

        if choice == "1":
            category = input("카테고리 (예: 식비, 교통 등): ")
            description = input("설명: ")
            try:
                amount = int(input("금액(원): "))
            except ValueError:
                print("잘못된 금액입니다.\n")
                continue
            budget.add_expense(category, description, amount)

        elif choice == "2":
            budget.list_expenses()

        elif choice == "3":
            budget.total_spent()

        elif choice == "4":
            if budget.backup_data():
                print("백업이 완료되었습니다.")

        elif choice == "5":
            backup_files = budget.list_backups()
            if backup_files:
                print("\n복원할 백업 파일을 선택하세요:")
                for idx, file in enumerate(backup_files, 1):
                    print(f"{idx}. {file}")
                try:
                    choice = int(input("\n선택 (숫자) > "))
                    if 1 <= choice <= len(backup_files):
                        budget.restore_data(backup_files[choice-1])
                    else:
                        print("잘못된 선택입니다.")
                except ValueError:
                    print("잘못된 입력입니다.")

        elif choice == "6":
            budget.list_backups()

        elif choice == "7":
            print("가계부를 종료합니다.")
            break

        else:
            print("잘못된 선택입니다.\n")


if __name__ == "__main__":
    main()

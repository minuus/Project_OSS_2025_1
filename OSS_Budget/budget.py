import datetime
import json
import os
from expense import Expense

class Budget:
    def __init__(self):
        self.expenses = []

    def add_expense(self, category, description, amount):
        today = datetime.date.today().isoformat()
        expense = Expense(today, category, description, amount)
        self.expenses.append(expense)
        print("지출이 추가되었습니다.\n")

    def list_expenses(self):
        if not self.expenses:
            print("지출 내역이 없습니다.\n")
            return
        print("\n[지출 목록]")
        for idx, e in enumerate(self.expenses, 1):
            print(f"{idx}. {e}")
        print()

    def total_spent(self):
        total = sum(e.amount for e in self.expenses)
        print(f"총 지출: {total}원\n")

    def backup_data(self):
        """현재 가계부 데이터를 백업 파일로 저장합니다."""
        if not os.path.exists('backups'):
            os.makedirs('backups')
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backups/budget_backup_{timestamp}.json"
        
        # 지출 데이터를 딕셔너리 리스트로 변환
        expenses_data = []
        for expense in self.expenses:
            expenses_data.append({
                'date': expense.date,
                'category': expense.category,
                'description': expense.description,
                'amount': expense.amount
            })
        
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(expenses_data, f, ensure_ascii=False, indent=2)
            print(f"\n백업이 성공적으로 생성되었습니다: {backup_file}")
            return True
        except Exception as e:
            print(f"\n백업 생성 중 오류가 발생했습니다: {str(e)}")
            return False

    def restore_data(self, backup_file):
        """백업 파일에서 가계부 데이터를 복원합니다."""
        if not os.path.exists(backup_file):
            print(f"\n백업 파일을 찾을 수 없습니다: {backup_file}")
            return False
        
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                expenses_data = json.load(f)
            
            # 데이터 검증
            for expense_data in expenses_data:
                required_fields = ['date', 'category', 'description', 'amount']
                if not all(field in expense_data for field in required_fields):
                    raise ValueError("유효하지 않은 백업 파일입니다.")
            
            # 현재 데이터 백업
            self.backup_data()
            
            # 데이터 복원
            self.expenses = []
            for expense_data in expenses_data:
                expense = Expense(
                    expense_data['date'],
                    expense_data['category'],
                    expense_data['description'],
                    expense_data['amount']
                )
                self.expenses.append(expense)
            
            print(f"\n데이터가 성공적으로 복원되었습니다.")
            return True
            
        except json.JSONDecodeError:
            print(f"\n잘못된 형식의 백업 파일입니다.")
            return False
        except Exception as e:
            print(f"\n데이터 복원 중 오류가 발생했습니다: {str(e)}")
            return False

    def list_backups(self):
        """사용 가능한 백업 파일 목록을 표시합니다."""
        if not os.path.exists('backups'):
            print("\n백업 파일이 없습니다.")
            return []
        
        backup_files = []
        print("\n[사용 가능한 백업 목록]")
        for file in os.listdir('backups'):
            if file.startswith('budget_backup_') and file.endswith('.json'):
                backup_files.append(os.path.join('backups', file))
                # 파일 생성 시간 표시
                timestamp = file[14:-5]  # 'budget_backup_' 제외, '.json' 제외
                date_time = datetime.datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                formatted_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"- {formatted_time} : {file}")
        
        if not backup_files:
            print("백업 파일이 없습니다.")
        print()
        return backup_files



import tkinter as tk
from tkinter import messagebox
import random
from words_database import WORDS_DICT

class WordGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("لعبة تخمين معاني الكلمات")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        # المتغيرات
        self.current_word = None
        self.current_meaning = None
        self.attempts = 0
        self.score = 0
        self.total_words = 0
        
        # الواجهة الرسومية
        self.setup_ui()
        self.new_game()
        
    def setup_ui(self):
        # العنوان الرئيسي
        title_label = tk.Label(
            self.root, 
            text="🎮 لعبة تخمين معاني الكلمات 🎮", 
            font=("Arial", 22, "bold"),
            bg="#f0f0f0",
            fg="#d32f2f"
        )
        title_label.pack(pady=20)
        
        # معلومات الكلمات المتوفرة
        info_label = tk.Label(
            self.root,
            text=f"عدد الكلمات المتاحة: {len(WORDS_DICT)} كلمة",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#666"
        )
        info_label.pack(pady=5)
        
        # عرض الكلمة
        self.word_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#0066cc"
        )
        self.word_label.pack(pady=15)
        
        # السؤال
        question_label = tk.Label(
            self.root,
            text="❓ ما معنى هذه الكلمة؟",
            font=("Arial", 14),
            bg="#f0f0f0",
            fg="#333"
        )
        question_label.pack(pady=10)
        
        # حقل الإدخال
        self.entry = tk.Entry(
            self.root,
            font=("Arial", 12),
            width=45,
            relief=tk.FLAT,
            bd=2
        )
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda e: self.check_answer())
        
        # زر التحقق
        check_button = tk.Button(
            self.root,
            text="✓ تحقق من الإجابة",
            command=self.check_answer,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=25,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2"
        )
        check_button.pack(pady=10)
        
        # عرض النتيجة
        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12),
            bg="#f0f0f0",
            wraplength=500
        )
        self.result_label.pack(pady=10)
        
        # عرض النقاط والمحاولات
        self.info_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="#1976d2"
        )
        self.info_label.pack(pady=5)
        
        # إطار للأزرار السفلية
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)
        
        # زر جديد
        new_button = tk.Button(
            button_frame,
            text="🔄 كلمة جديدة",
            command=self.new_game,
            font=("Arial", 11, "bold"),
            bg="#2196F3",
            fg="white",
            padx=15,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        new_button.pack(side=tk.LEFT, padx=5)
        
        # زر إعادة تعيين
        reset_button = tk.Button(
            button_frame,
            text="🔃 إعادة تعيين",
            command=self.reset_game,
            font=("Arial", 11, "bold"),
            bg="#ff9800",
            fg="white",
            padx=15,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        reset_button.pack(side=tk.LEFT, padx=5)
        
        # زر خروج
        exit_button = tk.Button(
            button_frame,
            text="❌ خروج",
            command=self.root.quit,
            font=("Arial", 11, "bold"),
            bg="#f44336",
            fg="white",
            padx=15,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        exit_button.pack(side=tk.LEFT, padx=5)
        
    def new_game(self):
        if len(WORDS_DICT) == 0:
            messagebox.showerror("خطأ", "لا توجد كلمات في القاموس!")
            return
            
        self.current_word = random.choice(list(WORDS_DICT.keys()))
        self.current_meaning = random.choice(WORDS_DICT[self.current_word])
        self.attempts = 0
        self.total_words += 1
        self.entry.delete(0, tk.END)
        self.result_label.config(text="", fg="black")
        self.word_label.config(text=f"📖 الكلمة: {self.current_word}")
        self.entry.focus()
        self.update_info()
        
    def check_answer(self):
        user_answer = self.entry.get().strip()
        
        if not user_answer:
            messagebox.showwarning("تحذير", "الرجاء إدخال إجابة!")
            return
        
        self.attempts += 1
        
        # مقارنة الإجابات بشكل أفضل
        if user_answer.lower() in self.current_meaning.lower() or \
           self.current_meaning.lower() in user_answer.lower():
            self.score += 1
            self.result_label.config(
                text=f"✅ صحيح! 🎉\nالمعنى: {self.current_meaning}",
                fg="#4CAF50"
            )
            self.update_info()
            self.root.after(2500, self.new_game)
        else:
            if self.attempts < 3:
                self.result_label.config(
                    text=f"❌ خطأ! حاول مرة أخرى (المحاولة {self.attempts}/3)\nالمعنى الصحيح: {self.current_meaning}",
                    fg="#f44336"
                )
                self.entry.delete(0, tk.END)
                self.entry.focus()
            else:
                self.result_label.config(
                    text=f"⏹️ انتهت المحاولات!\nالمعنى الصحيح: {self.current_meaning}",
                    fg="#d32f2f"
                )
                self.root.after(2500, self.new_game)
                
        self.update_info()
        
    def reset_game(self):
        response = messagebox.askyesno("تأكيد", "هل تريد إعادة تعيين النقاط والإحصائيات؟")
        if response:
            self.score = 0
            self.total_words = 0
            self.new_game()
            messagebox.showinfo("تم", "تم إعادة تعيين اللعبة بنجاح!")
        
    def update_info(self):
        accuracy = 0
        if self.total_words > 0:
            accuracy = (self.score / self.total_words) * 100
        
        self.info_label.config(
            text=f"📊 النقاط: {self.score} | الكلمات: {self.total_words} | الدقة: {accuracy:.1f}% | المحاولة: {self.attempts}/3"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = WordGameApp(root)
    root.mainloop()

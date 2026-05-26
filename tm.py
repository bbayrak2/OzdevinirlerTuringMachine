import re

class TuringMachine:
    def __init__(self, n1, n2):

        tape_str = f"{n1}*{n2}="
        self.tape = list(tape_str)
        self.head = 0 
        self.state = 'q_baslangic'
        self.log = []
        self.macro_steps = []
        
    def read(self):
        if self.head >= len(self.tape):
            self.tape.extend(['_'] * (self.head - len(self.tape) + 1))
        return self.tape[self.head]
        
    def write(self, symbol):
        self.tape[self.head] = symbol
        
    def move(self, direction):
        if direction == 'R':
            self.head += 1
        elif direction == 'L':
            self.head -= 1
            if self.head < 0:
                self.tape.insert(0, '_')
                self.head = 0 
        elif direction == 'S':
            pass 
            
    def action(self, next_state, write_sym, direction):
        read_sym = self.read()
        
        tape_display = []
        for i, sym in enumerate(self.tape):
            if i == self.head:
                tape_display.append(f"[{sym}]")
            else:
                tape_display.append(sym)
      
        tape_str = "".join(tape_display).rstrip('_') + "_"

        self.log.append({
            'state': self.state,
            'read': read_sym,
            'write': write_sym,
            'move': direction,
            'tape': tape_str
        })
        
        self.write(write_sym)
        self.move(direction)
        self.state = next_state

    def run(self):
        while self.read() not in ['*', '_']:
            self.action('q_yildiz_ara', self.read(), 'R')
            
        if self.read() == '*':
            self.action('q_yildiz_bulundu', '*', 'L')
            self.macro_steps.append("Adım 1: '*' bulundu -> operandlar ayrıldı.")
        else:
            self.action('q_red', '_', 'S')
            print("HATA: Bantta '*' bulunamadı.")
            return

        multiplicand_bits = []
        self.state = 'q_carpan1_oku'
        while True:
            multiplicand_bits.insert(0, self.read())
            if self.head == 0: 
                self.action('q_yildiza_don', self.read(), 'R')
                break
            self.action('q_carpan1_oku', self.read(), 'L')
            
        while self.read() != '*':
            self.action('q_yildiza_don', self.read(), 'R')
            
        self.action('q_esittir_ara', '*', 'R') 
        while self.read() != '=':
            self.action('q_esittir_ara', self.read(), 'R')
            
        self.action('q_carpan2_oku', '=', 'L') 
        multiplier_bits = []
        while self.read() != '*':
            multiplier_bits.insert(0, self.read())
            self.action('q_carpan2_oku', self.read(), 'L')
            
        while self.read() != '=':
            self.action('q_sonuc_hazirlik', self.read(), 'R')

        result = 0
        shifted_m = int("".join(multiplicand_bits), 2)
        base_m_str = "".join(multiplicand_bits)
        
        shift_amount = 0
        step_num = 2
        for bit in reversed(multiplier_bits):
            current_shifted_str = base_m_str + ("0" * shift_amount)
            if bit == '0':
                self.macro_steps.append(f"Adım {step_num}: sağdan bit = 0 -> işlem yapılmadı")
            else:
                result += shifted_m
                self.macro_steps.append(f"Adım {step_num}: sıradaki bit = 1 -> {base_m_str} sola kaydırıldı -> {current_shifted_str}. (Eklendi)")
            
            shifted_m <<= 1
            shift_amount += 1
            step_num += 1
            
        self.macro_steps.append(f"Adım {step_num}: sonuç yazıldı.")
        
        result_bin = bin(result)[2:]
        self.action('q_sonuc_yaz', '=', 'R') 
        for bit in result_bin:
            self.action('q_sonuc_yaz', bit, 'R')
            
        self.action('q_kabul', '_', 'S')
        self.final_result_bin = result_bin
        self.final_result_dec = result

def main():
    print("-" * 50)
    print(" TURING MAKİNESİ - BINARY ÇARPMA SİMÜLATÖRÜ ")
    print("-" * 50)
    
    while True:
        n1 = input("Birinci sayı (Binary): ").strip()
        n2 = input("İkinci sayı (Binary): ").strip()
        
        if re.fullmatch(r'[01]+', n1) and re.fullmatch(r'[01]+', n2):
            break
        print("HATA: Lütfen sadece '0' ve '1' karakterlerini içeren geçerli binary sayılar giriniz!\n")
        
    print("\n[+] Bant başlatılıyor...")
    tm = TuringMachine(n1, n2)
    tm.run()
    
    print("\n--- TURING MAKİNESİ ADIM ADIM ÇALIŞMA TABLOSU ---")
    print(f"{'Mevcut Durum':<20} | {'Okuma':<5} | {'Yazma':<5} | {'Yön':<3} | {'Bant İçeriği'}")
    print("-" * 80)
    for log in tm.log:
        print(f"{log['state']:<20} | {log['read']:<5} | {log['write']:<5} | {log['move']:<3} | {log['tape']}")
        
    print("\n--- KAYDIR VE TOPLA (SHIFT & ADD) MANTIĞI ---")
    for step in tm.macro_steps:
        print(step)
        
    print("\n--- SONUÇ ---")
    print(f"Banttaki İşlem : {n1} * {n2} = {tm.final_result_bin}")
    print(f"Binary Sonuç   : {tm.final_result_bin}")
    print(f"Decimal Sonuç  : {int(n1, 2)} * {int(n2, 2)} = {tm.final_result_dec}")
    print("-" * 50)

if __name__ == "__main__":
    main()

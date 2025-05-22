import tkinter as tk
from tkinter import messagebox
import random

# Configurações iniciais
money = 0
click_value = 1
click_upgrade_cost = 50
passive_income = 0
passive_upgrade_cost = 100


def update_money_label():
    """Atualiza o rótulo de dinheiro."""
    money_label.config(text=f"Dinheiro: R$ {money:.2f}")


def add_particle(value, x, y):
    """Cria partículas animadas no local do clique."""
    particle = tk.Label(root, text=f"+R$ {value}", fg="green", font=("Arial", 12))
    particle.place(x=x, y=y)

    def move_particle():
        nonlocal y
        y -= 2
        particle.place(x=x, y=y)
        if y > -20:
            root.after(50, move_particle)
        else:
            particle.destroy()

    move_particle()


def click_button(event=None):
    """Função chamada ao clicar no botão."""
    global money
    money += click_value
    update_money_label()
    add_particle(click_value, random.randint(200, 300), random.randint(150, 200))


def upgrade_click():
    """Compra upgrade para aumentar valor do clique."""
    global money, click_value, click_upgrade_cost
    if money >= click_upgrade_cost:
        money -= click_upgrade_cost
        click_value += 1
        click_upgrade_cost *= 1.5
        update_money_label()
        messagebox.showinfo("Upgrade", f"Agora você ganha R$ {click_value} por clique!")
    else:
        messagebox.showwarning("Sem dinheiro!", "Dinheiro insuficiente para este upgrade.")


def upgrade_passive():
    """Compra upgrade para ganhar dinheiro passivo."""
    global money, passive_income, passive_upgrade_cost
    if money >= passive_upgrade_cost:
        money -= passive_upgrade_cost
        passive_income += 1
        passive_upgrade_cost *= 2
        update_money_label()
        messagebox.showinfo("Upgrade", f"Agora você ganha R$ {passive_income} por segundo!")
    else:
        messagebox.showwarning("Sem dinheiro!", "Dinheiro insuficiente para este upgrade.")


def passive_earnings():
    """Gera dinheiro passivo a cada segundo."""
    global money
    money += passive_income
    update_money_label()
    root.after(1000, passive_earnings)


# Configuração da janela principal
root = tk.Tk()
root.title("Jogo de Clique")
root.geometry("400x400")

# Rótulo de dinheiro
money_label = tk.Label(root, text=f"Dinheiro: R$ {money:.2f}", font=("Arial", 16))
money_label.pack(pady=10)

# Botão principal
click_btn = tk.Button(root, text="Clique aqui!", font=("Arial", 16), bg="lightblue", command=click_button)
click_btn.pack(pady=20)

# Botão de upgrade de clique
click_upgrade_btn = tk.Button(
    root,
    text=f"Upgrade: +1 por clique (R$ {click_upgrade_cost:.2f})",
    font=("Arial", 12),
    command=upgrade_click,
)
click_upgrade_btn.pack(pady=10)


def update_click_upgrade_button():
    """Atualiza o texto do botão de upgrade de clique."""
    click_upgrade_btn.config(text=f"Upgrade: +1 por clique (R$ {click_upgrade_cost:.2f})")
    root.after(100, update_click_upgrade_button)


# Botão de upgrade de renda passiva
passive_upgrade_btn = tk.Button(
    root,
    text=f"Upgrade: +1 por segundo (R$ {passive_upgrade_cost:.2f})",
    font=("Arial", 12),
    command=upgrade_passive,
)
passive_upgrade_btn.pack(pady=10)


def update_passive_upgrade_button():
    """Atualiza o texto do botão de upgrade de renda passiva."""
    passive_upgrade_btn.config(text=f"Upgrade: +1 por segundo (R$ {passive_upgrade_cost:.2f})")
    root.after(100, update_passive_upgrade_button)


# Iniciar o loop de renda passiva
root.after(1000, passive_earnings)
update_click_upgrade_button()
update_passive_upgrade_button()

# Inicia a janela
root.mainloop()

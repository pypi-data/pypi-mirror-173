#Simples calculadora utilizando funções e While.

opcao = True

def soma():
    numero_1 = float(input("   Digite o primeiro número: "))
    numero_2 = float(input("   Digite o segundo número: "))
    print("   Resultado da soma: ", numero_1 + numero_2)


def subtracao():
    numero_1 = float(input("   Digite o primeiro número: "))
    numero_2 = float(input("   Digite o segundo número: "))
    print("   Resultado da subtração: ", numero_1 - numero_2)

def multiplicacao():
    numero_1 = float(input("   Digite o primeiro número: "))
    numero_2 = float(input("   Digite o segundo número: "))
    print("   Resultado da multiplicação: ", numero_1 * numero_2)

def divisao():
    numero_1 = float(input("   Digite o primeiro número: "))
    numero_2 = float(input("   Digite o segundo número: "))
    print("   Resultado da divisão: ", numero_1 / numero_2)


while (opcao):

    print("--------------- Menu Calculadora Simples --------------- \n")
    print("   1. Somar")
    print("   2. Subtrair")
    print("   3. Multiplicação")
    print("   4. Divisão")
    print("   5. Sair\n")
    print("-------------------------------------------------------- \n")
    escolha = (input("   Bem vindo! Digite a opção desejada conforme menu acima: "))
        
    if(escolha == "1"):
        soma()
        decisao = input("   Aperte a tecla número 5 para sair do programa ou qulquer outra tecla para voltar ao menu: ")
        if (decisao == "5"):
            print("   Saindo do programa, até breve! ")
            opcao = False
        else:
            opcao = True
            escolha = 0

    elif(escolha == "2"):
        subtracao()
        decisao = input("   Aperte a tecla número 5 para sair do programa ou qulquer outra tecla para voltar ao menu: ")
        if (decisao == "5"):
            print("   Saindo do programa, até breve! ")
            opcao = False
        else:
            opcao = True
            escolha = 0

    elif(escolha == "3"):
        multiplicacao()
        decisao = input("   Aperte a tecla número 5 para sair do programa ou qulquer outra tecla para voltar ao menu: ")
        if (decisao == "5"):
            print("   Saindo do programa, até breve! ")
            opcao = False
        else:
            opcao = True
            escolha = 0

    elif(escolha == "4"):
        divisao()
        decisao = input("   Aperte a tecla número 5 para sair do programa ou qulquer outra tecla para voltar ao menu: ")
        if (decisao == "5"):
            print("   Saindo do programa, até breve! ")
            opcao = False
        else:
            opcao = True
            escolha = 0

    elif(escolha == "5"):
        print("   Saindo do programa, até breve! ")
        break

    else:
        print("Opção inválida!")

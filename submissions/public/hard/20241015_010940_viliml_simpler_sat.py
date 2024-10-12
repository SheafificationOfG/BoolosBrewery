from itertools import permutations, product
from math import comb as comb_number

from strats import *

keys = 0x100300901b0520530f90fa01c05405510010105610210310401d05705810810905910b10d00a01e05a05b05c11411511601f05d05e11a11b11c05f11d11e11f02006006112412506212612712800b02106306406512f13013102206606713513613706813813913a02306906a13f14006b14114214300400c02406c06d06e14a14b14c02506f07015015115207115415502607207315a15b07415c15d15e00d02707507607716516616702807807916b16c16d07a16e17002907b07c17417517607d00e02a07e07f08018018118202b08108218718808318918a18b02c08408518f19108619319400500f02d08708808919b19c19d02e08a08b1a21a308c1a41a51a602f08d08e1ab1ac08f1ad1ae1af0100300900910921b61b71b80310930941bc1bd0951bf1c10320960971c61c70981c81c91ca01103309909a09b1d11d21d303409c09d1d71d809e1da1dc03509f0a01e11e20a11e41e5
vals = 0xbfb1d6ac6d274462ae0c2ab37fc33c9e886026a2be0da8cf39fb9b61c90bc5fe9019d0ff000b0126c30b68c03445c17f886d43766f0b128f9c9931096715e4f11205f93bd1271c4fd0000000000000000000000000000000000000d3ffff25f539f5a9d5db141eb9e327eb890a45000000000000000000000000000000000000f000000000000000000000000000000000000d000000266b61c6bbabfb5e95703dd26f9f88000000000000000000000000000000000000033ffffffffa17405d51f4313ef2e024b45f114000000000000000000000000000000000000000000000000000000000000000000000000063fe44bca02ea0fc19a5d87447590e9ef5cf340000000000000000000000000000000000009000000000000000000000000000000000000100000000000000000000000000000000000070003a4e38040b561f987a681af1f7b722972600000000000000000000000000000000000023ff900aa5da2f0906703e20b73d8f86e8a836000000000000000000000000000000000001600000000000000000000000000000000000083fffe0ce38522700de362656dfcb98ffb7aae000000000000000000000000000000000000e000000000000000000000000000000000000c000007b599570a240a164ff3a84935daa44a43b05166cb32c90399cf6a40621298fbe523010000000000000000000000000000000000007000000000000000000000000000000000000f3fffffffcd086fcc306d532c360156111773c0000000000000000000000000000000000009000000000000000000000000000000000000300000000000000000000000000000000000010000008080b46e9b368b64e9758da7af5764c00000000000000000000000000000000000083ffffec872e599fa9f5725be99990b1f0c06e000000000000000000000000000000000000e0000000000000000000000000000000000002000000000000000000000000000000000000c3fffffff707c69a19e79c7c0276fce8bff4d9000000000000000000000000000000000000300000000000000000000000000000000000060000000000000000000000000000000000000000bed70cdb84391b5915de10bd6f25b12ba0000000000000000000000000000000000000a3fffba30e9716264fec594f6ec77d05bbf40c0000000000000000000000000000000000005000000000000000000000000000000000000b3ffffffffe0f12422d23e0f2b0d4a945575ae0000000000000000000000000000000000011000000000000000000000000000000000001000000000000000000000000000000000000040028b9d61654136df3a8f07e05f768bcb033d0c825eea038c6ff8404726cdb7af06a575157000000000000000000000000000000000000f00000000000000000000000000000000000093e95aa29cf21491a42e7e79997ceedaae5010000000000000000000000000000000000000100000000000000000000000000000000000070000000000000000000000000000000000009053d50792913f547a9c51c444b989a775625100000000000000000000000000000000000123fb681e4e9f0e15c10b1dacf027192728c0060000000000000000000000000000000000017000000000000000000000000000000000001400000000000000000000000000000000000163fffbfbcfb8034d549a24d80d3c27f57e5fa4000000000000000000000000000000000000d00000000000000000000000000000000000060000000000000000000000000000000000000000fa7c5a26158ffe52dcf9ce8244142fed61000000000000000000000000000000000000c3ffffff82d6c2b572c48ab9dcfe85f3339a61000000000000000000000000000000000001500000000000000000000000000000000000133fffff9f654763bbbf4d85254ff2764f03f0600000000000000000000000000000000000020000000000000000000000000000000000008000000000000000000000000000000000000e0000028357988a05c87a1d56ea7a5db9380b80000003026de9efe49004df5ae20e2e32fe1b3cdbb166e29b4e0a8504e031ff31624ba0b9d000000000000000000000000000000000001500000000000000000000000000000000000123ffffa327a51f49e5f19b34eff25c1a88e901000000000000000000000000000000000001300000000000000000000000000000000000140000000000000000000000000000000000003000001184c8c746267adb4abe9efe8322adeb00000000000000000000000000000000000173ffffd512b58c96dcc7f3f6a437350c1798580000000000000000000000000000000000007000000000000000000000000000000000000300000000000000000000000000000000000013ffffce32e1cff185aac27198a9fdb4655eaf000000000000000000000000000000000000d000000000000000000000000000000000000f0018e44eac6919a63edf08861c8c2e9f4ee23000000000000000000000000000000000000b3ff84f7dc3d2a428eca7f6aa11ccf1a600bfb000000000000000000000000000000000001100000000000000000000000000000000000103ffece2af6197466952cb267b2d9e78e2e5d800000000000000000000000000000000000070000000000000000000000000000000000004000000000000000000000000000000000000500000000015399b53bc42edaf077e9cf2c2fb2e94f596684d0f32b0ef80e9d475679b6b3bd000000000000000000000000000000000000200000000000000000000000000000000000123ffb73f355c849ba9ee7a6b70bac715b8543900000000000000000000000000000000000130000000000000000000000000000000000014000000000000000000000000000000000001500001e54b7b345a10f777b2b0eb5f0d4eaea800000000000000000000000000000000000171422aa85188d0cc5ed8313fecd713efdc41e30000000000000000000000000000000000017000000000000000000000000000000000000900000000000000000000000000000000000033fffffd65847a10d922f46ed78cd03c39ecbd0000000000000000000000000000000000002000000000000000000000000000000000001700004d0684eeb17db67e92826f01763a9d934000000000000000000000000000000000000a3fffead81ad6a94cffa0ac4b1a7a0f5255869000000000000000000000000000000000000d0000000000000000000000000000000000001000000000000000000000000000000000000f0000000000000000000000000000000000002000001cc77f3730cf96ce59d1eca6585abad1090630575651874f47ac5f7ac63db2a9f4c54000000000000000000000000000000000000000000000000000000000000000000000000083cff37cfa3fd6f2e1fac6a4fa96699a7c2521000000000000000000000000000000000000c000000000000000000000000000000000000e000000000000000000000000000000000000600029cc67f8962ac3bd213935dd596b950be000000000000000000000000000000000000093fffffffbed5e5663ffe7ae93177372c208cc000000000000000000000000000000000000700000000000000000000000000000000000013fffdb9e6d2855b04a58b4090bc65057fefdf000000000000000000000000000000000000d000000000000000000000000000000000000f000000000000000000000000000000000000300000002eaea0d65ae0531fb60e19fdd8189a00000000000000000000000000000000000173ff771b73a02d1dba0298048b430eb770ce93000000000000000000000000000000000001300000000000000000000000000000000000153fd642767e4ea7fce0d0b30aebfa8d524257e000000000000000000000000000000000001400000000000000000000000000000000000120037c5e9f7e5912b0af56fe05519a7ef13da900002f901ee99d7a61ac0de18cfbbb448d50b2171071fb5604f6ffc24de7a3bd313b9c1006000000000000000000000000000000000001000000000000000000000000000000000000043fedca2d8ac626725ee3ce1d767e046c49ca8000000000000000000000000000000000000b0000000000000000000000000000000000005000000000000000000000000000000000000a0002cd8437a805c02c4798f2521da47a9f73600000000000000000000000000000000000123ffe762876a9f66c0cb55d5cde55e98c069e2000000000000000000000000000000000001700000000000000000000000000000000000163ffffc77ba6157b90bb71e9d1c6374968915d00000000000000000000000000000000000130000000000000000000000000000000000015000000000000000000000000000000000001400035d15071281259bc2ca5d00f62ebc72c6f00000000000000000000000000000000000113ffd43eeaa539fbc56791f44caf83bc6d5d1c000000000000000000000000000000000000300000000000000000000000000000000000093ffffdaeab9f0e23016530ced046890d24781000000000000000000000000000000000000d0000000000000000000000000000000000001000000000000000000000000000000000000f001432658f4cacca758394965231f68d331e8049932737390bcc46eefa9282207d6071eb1e0000000000000000000000000000000000002000000000000000000000000000000000000c3fef55d7f85dd105b0ad72d8ade5e0e0d242800000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000000000000000800cecaee28c9871f3c542bad238ec6ae1852f00000000000000000000000000000000000113ffd3d756d6879212cf4a28e14d8023e38d9f000000000000000000000000000000000000b00000000000000000000000000000000000053ffff5b145aeb5f66c523407c48f3812a0f2f0000000000000000000000000000000000010000000000000000000000000000000000000701c3c5196e05c67990be21ca30b1d0656c2a400000000000000000000000000000000000093fffedf18d080fc1c699f44e31015dba8eb3a0000000000000000000000000000000000004000000000000000000000000000000000000a3fffff9125b1bbf6ea3bd5699d86273db979f000000000000000000000000000000000000d000000000000000000000000000000000000f00000000000000000000000000000000000030009659a43308ba6eb2556d851ec48717b0700051be2b68749b1941e9d07bad92a5d1c08690000000000000000000000000000000000001000000000000000000000000000000000000e3fffffffffe920e68d825b3d9f3f5ef0366230000000000000000000000000000000000003000000000000000000000000000000000000d000000000000000000000000000000000000f00000763f2465c9791c5e7936f7a73ae1fe9700000000000000000000000000000000000053fffe130af3b83b1a90bebe1e5f8494eb4a5f000000000000000000000000000000000000b00000000000000000000000000000000000093ffff0ce86af2ccb09fba00f00ced88d300cf0000000000000000000000000000000000010000000000000000000000000000000000001100010a1bea1db0304d5699c7f2c84b7825a7400000000000000000000000000000000000073fffffb8ad6234fb80c9cc569907ecaa02ec10000000000000000000000000000000000001000000000000000000000000000000000000708ea690c730942dc79c93af1fcf84fe246ee2000000000000000000000000000000000000a0000000000000000000000000000000000004
data = dict((keys // 4096**i % 4096, vals // 16**(37*i) % 16**37) for i in range(231))

def get_combination_by_index(n, index):
    combination = []
    current_index = index
    k = 0

    while True:
        if current_index < comb_number(n, k):
            break
        current_index -= comb_number(n, k)
        k += 1

    remaining_elements = k

    for i in range(n):
        if remaining_elements == 0:
            break

        comb_with_i = comb_number(n - i - 1, remaining_elements - 1)
        if comb_with_i <= current_index:
            current_index -= comb_with_i
        else:
            combination.append(i)
            remaining_elements -= 1

    return tuple(combination)


data_table = {
    k: dat if dat < 24 else (get_combination_by_index(144, dat // 4), dat % 4)
    for k, dat in data.items()
}

respuestas_list = [
    Foo,
    Bar,
    Baz,
]
fields_list = [
    "Math",
    "Phys",
    "Phil",
    "Engg",
]
personas_list = [
    Alice,
    Bob,
    Charlie,
    Dan,
]

# f = order of responses      i = the order of the persons
perm_escenarios = list(product(permutations(range(3)), permutations(range(4))))


def get_question(node):
    final_question = "False"
    for var in node[0]:
        orden_respuestas, orden_fields = perm_escenarios[var]
        question = "True"

        for persona, orden_field, field, orden_respuesta in zip(personas_list, orden_fields, fields_list, orden_respuestas):
            question += f" and ({persona} studies {fields_list[orden_field]})"
            if field != "Engg":
                question += f' and ("{field}: 1?" is {respuestas_list[orden_respuesta]})'

        final_question += f" or ({question})"

    return node[1], final_question


class Strategy(Hard):
    question_limit = 5

    def solve(self):
        nodo_actual = 1

        while isinstance(data_actual := data_table[nodo_actual], tuple):
            asker, question = get_question(data_actual)
            nodo_actual *= 3
            nodo_actual += respuestas_list.index(self.get_response(personas_list[asker].ask(question)))

        for game_persona, field in zip(personas_list, perm_escenarios[data_actual][1]):
            self.guess[game_persona] = Field(fields_list[field])
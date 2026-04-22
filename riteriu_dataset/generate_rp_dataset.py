#!/usr/bin/env python3
"""Generate knights-and-knaves puzzles as JSONL.

This script mirrors the puzzle generation logic from js/knaves.js and outputs
40 easy, 40 medium, and 20 hard puzzles by default.
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from typing import List, Optional


ACTIVE_LANGUAGE = "en"


ORIGINAL_NAME_SET = [
    "Alice",
    "Bob",
    "Carol",
    "Dave",
    "Edward",
    "Francine",
    "Gary",
    "Henry",
    "Ingrid",
    "Joan",
    "Kevin",
    "Lisa",
    "Mike",
    "Neil",
    "Owen",
    "Pat",
    "Quinn",
    "Rachel",
    "Sally",
    "Trevor",
    "Unis",
    "Victoria",
    "Wallace",
    "Xavier",
    "Yasmin",
    "Zelda",
]

ORIGINAL_NAME_SET_1 = [
    "Arthur",
    "Beatrix",
    "Connor",
    "Denise",
    "Eustice",
    "Frank",
    "Gwen",
    "Hillary",
    "Ira",
    "Justin",
    "Kirstin",
    "Larry",
    "Michelle",
    "Nancy",
    "Oberon",
    "Pamela",
    "Quentin",
    "Robert",
    "Samuel",
    "Tracy",
    "Uri",
    "Vincent",
    "Wendy",
    "Xan",
    "Yuri",
    "Zoro",
]

LITHUANIAN_NAME_SET = [
    "Aiste",
    "Benas",
    "Dovile",
    "Egle",
    "Gabija",
    "Giedrius",
    "Ieva",
    "Inga",
    "Jonas",
    "Jurate",
    "Karolis",
    "Kestutis",
    "Lina",
    "Mantas",
    "Milda",
    "Neringa",
    "Paulius",
    "Rasa",
    "Ruta",
    "Saulius",
    "Simona",
    "Tadas",
    "Tomas",
    "Ugne",
    "Vaida",
    "Vytautas",
]

LITHUANIAN_NAME_SET_1 = [
    "Adomas",
    "Aurelijus",
    "Ausrine",
    "Daiva",
    "Deimante",
    "Donatas",
    "Edita",
    "Eimantas",
    "Emilija",
    "Ernestas",
    "Gintare",
    "Greta",
    "Jolanta",
    "Laimis",
    "Laura",
    "Lukas",
    "Martynas",
    "Monika",
    "Nida",
    "Remigijus",
    "Rokas",
    "Skirmante",
    "Viktorija",
    "Vilius",
    "Zivile",
    "Zygimantas",
]


def name_set() -> List[str]:
    if ACTIVE_LANGUAGE == "lt":
        return random.choice([LITHUANIAN_NAME_SET_1, LITHUANIAN_NAME_SET]).copy()
    return random.choice([ORIGINAL_NAME_SET_1, ORIGINAL_NAME_SET]).copy()


def random_int(less_than: int) -> int:
    return random.randrange(less_than)


def random_range(greater_than: int, less_than: int) -> int:
    return random.randint(greater_than, less_than)


def random_element(items: List):
    return random.choice(items)


def shuffle(items: List):
    random.shuffle(items)
    return items


def pretty_print_list(items: List[str]) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        joiner = "ir" if ACTIVE_LANGUAGE == "lt" else "and"
        return f"{items[0]} {joiner} {items[1]}"
    if ACTIVE_LANGUAGE == "lt":
        return ", ".join(items[:-1]) + f" ir {items[-1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"


def variable_name_pairs(names: List[str]) -> str:
    pairs = names.copy()
    if not pairs:
        return ""
    if len(pairs) == 1:
        return pairs[0]
    if len(pairs) == 2:
        joiner = "ir" if ACTIVE_LANGUAGE == "lt" else "and"
        return f"{pairs[0]} {joiner} {pairs[1]}"
    if ACTIVE_LANGUAGE == "lt":
        return ", ".join(pairs[:-1]) + f" ir {pairs[-1]}"
    return ", ".join(pairs[:-1]) + f", and {pairs[-1]}"


def build_prompt(islanders: List[str], statements: List[str]) -> str:
    n = len(islanders)
    vars_text = variable_name_pairs(islanders)
    statements_text = " ".join(statements)

    if ACTIVE_LANGUAGE == "lt":
        return (
            "Ypatingoje saloje gali gyventi tik dviejų tipų gyventojai: riteriai ir melagiai. "
            "Tarp jų gali būti, kad visi yra riteriai, visi yra melagiai, arba kai kurie yra riteriai, o kai kurie melagiai. "
            "Riteriai visada sako tiesą, o melagiai visada meluoja. "
            f"Sutinkate {n} gyventojus: {vars_text}. "
            f"{statements_text} "
            "Taigi kas yra riteris, o kas melagis?"
        )

    return (
        "A very special island is inhabited only by knights and knaves. "
        "Among them, it is possible that all are knights, all are knaves, or some are knights and some are knaves. "
        "Knights always tell the truth, and knaves always lie. "
        f"You meet {n} inhabitants: {vars_text}. "
        f"{statements_text} "
        "So who is a knight and who is a knave?"
    )


def text(key: str) -> str:
    texts = {
        "en": {
            "says": "says",
            "knave": "knave",
            "knight": "knight",
            "for_these_reasons": "For these reasons we know",
            "no_knaves": " there were no knaves",
            "only_knave": " the only knave was ",
            "knaves_were": " the knaves were ",
            "and_no_knights": ", and there were no knights.",
            "and_only_knight": ", and the only knight was ",
            "and_knights_were": ", and the knights were ",
            "you_said_no_knaves": "There were no knaves,",
            "you_said_one_knave": "The one knave was ",
            "you_said_knaves": "The knaves were ",
            "and_that_no_knights": " and that there were no knights.",
            "and_that_one_knight": " and that the one knight was ",
            "and_that_knights": " and that the knights were ",
            "you_were_right": "",
            "you_were_wrong": " You were wrong.",
            "there_were_no_knaves": " There were no knaves",
            "the_only_knave": " The only knave was ",
            "the_knaves_were": " The knaves were ",
        },
        "lt": {
            "says": "sako",
            "knave": "melagis",
            "knight": "riteris",
            "for_these_reasons": "Todėl žinome",
            "no_knaves": " melagių nebuvo",
            "only_knave": " vienintelis melagis buvo ",
            "knaves_were": " melagiai buvo ",
            "and_no_knights": ", o riterių nebuvo.",
            "and_only_knight": ", o vienintelis riteris buvo ",
            "and_knights_were": ", o riteriai buvo ",
            "you_said_no_knaves": "Melagių nebuvo,",
            "you_said_one_knave": "Vienintelis melagis buvo ",
            "you_said_knaves": "Melagiai buvo ",
            "and_that_no_knights": " o riterių nebuvo.",
            "and_that_one_knight": " o vienintelis riteris buvo ",
            "and_that_knights": " o riteriai buvo ",
            "you_were_right": "",
            "you_were_wrong": " Jūs klydote.",
            "there_were_no_knaves": " Melagių nebuvo",
            "the_only_knave": " Vienintelis melagis buvo ",
            "the_knaves_were": " Melagiai buvo ",
        },
    }
    return texts[ACTIVE_LANGUAGE][key]


def map_difficulty_label(label: str) -> str:
    if ACTIVE_LANGUAGE == "lt":
        mapping = {"easy": "lengvas", "medium": "vidutinis", "hard": "sunkus"}
        return mapping[label]
    return label


def array_without_element(items: List, elem):
    return [x for x in items if x is not elem]


def remove_element(items: List, elem):
    return [x for x in items if x is not elem]


def array_contains(items: List, elem) -> bool:
    return any(x is elem for x in items)


def arrays_equivalent(a: List, b: List) -> bool:
    if len(a) != len(b):
        return False
    if len(a) == 0:
        return True
    return all(array_contains(a, x) for x in b) and all(array_contains(b, x) for x in a)


def add_unique(items: List, elem):
    if not array_contains(items, elem):
        items.append(elem)
    return items


def add_all_unique(a: List, b: List):
    for item in b:
        add_unique(a, item)
    return a


def array_difference(a: List, b: List):
    out = a.copy()
    for x in b:
        out = remove_element(out, x)
    return out


class Islander:
    def __init__(self, name: str):
        self.name = name

    def match_statement_for(self, i: "Islander"):
        if i.is_knight():
            return Sympathetic(self, i)
        return Antithetic(self, i)

    def __str__(self):
        return self.name


class Knave(Islander):
    def is_knight(self) -> bool:
        return False

    def statement_for(self, i: Islander):
        if i.is_knight():
            return Accusation(self, i)
        return Affirmation(self, i)

    def compound_statement_for(self, i: Islander):
        return Joint(self, i)

    def type(self) -> str:
        return text("knave")


class Knight(Islander):
    def is_knight(self) -> bool:
        return True

    def statement_for(self, i: Islander):
        if i.is_knight():
            return Affirmation(self, i)
        return Accusation(self, i)

    def compound_statement_for(self, i: Islander):
        return Disjoint(self, i)

    def type(self) -> str:
        return text("knight")


class Statement:
    def __init__(self, source: Islander, target: Islander):
        self.source = source
        self.target = target
        self.text = self.build_statement()

    def build_statement(self) -> str:
        raise NotImplementedError

    def full_statement(self) -> str:
        return f"{self.source.name} {text('says')}: {self.text}."


class TypeStatement(Statement):
    def done(self, solver: "Solver") -> bool:
        has_target = array_contains(solver.knights, self.target) or array_contains(solver.knaves, self.target)
        has_source = array_contains(solver.knights, self.source) or array_contains(solver.knaves, self.source)
        return has_target and has_source

    def process(self, known: Islander, solver: "Solver"):
        if self.source is known or self.target is known:
            islanders = [self.source, self.target]
            unknown = remove_element(islanders, known)[0]
            solver.reasoning.append(self.reasoning(known))
            if unknown.is_knight():
                add_unique(solver.knights, unknown)
            else:
                add_unique(solver.knaves, unknown)

    def solve(self, solver: "Solver"):
        solver.type_statements.append(self)


class Accusation(TypeStatement):
    def build_statement(self) -> str:
        if ACTIVE_LANGUAGE == "lt":
            options = [
                " meluoja",
                " yra melagis",
                " visada meluoja",
                " niekada nesako tiesos",
                " meluoja",
                " sako netiesą",
            ]
        else:
            options = [
                " is lying",
                " is a knave",
                " always lies",
                " never tells the truth",
                " lies",
                " is untruthful",
            ]
        return self.target.name + random_element(options)

    def reasoning(self, known: Islander) -> str:
        unknown = remove_element([self.source, self.target], known)[0]
        if ACTIVE_LANGUAGE == "lt":
            return (
                "Visi salos gyventojai priešingo tipo žmogų vadins melagiu. "
                f"Todėl kai {self.source} sako, kad {self.target} yra melagis, žinome, kad "
                f"{self.target} ir {self.source} yra priešingų tipų. "
                f"Kadangi {known} yra {known.type()}, tada {unknown} yra {unknown.type()}."
            )
        return (
            "All islanders will call a member of the opposite type a knave. "
            f"So when {self.source} says that {self.target} is a knave, we know that "
            f"{self.target} and {self.source} are opposite types. "
            f"Since {known} is a {known.type()}, then {unknown} is a {unknown.type()}."
        )


class Affirmation(TypeStatement):
    def build_statement(self) -> str:
        if ACTIVE_LANGUAGE == "lt":
            options = [
                " sako tiesą",
                " yra riteris",
                " visada sako tiesą",
                " niekada nemeluoja",
                " sako tiesą",
            ]
        else:
            options = [
                " is truthful",
                " is a knight",
                " always tells the truth",
                " never lies",
                " tells the truth",
            ]
        return self.target.name + random_element(options)

    def reasoning(self, known: Islander) -> str:
        unknown = remove_element([self.source, self.target], known)[0]
        if ACTIVE_LANGUAGE == "lt":
            return (
                "Visi salos gyventojai savo tipo žmogų vadins riteriu. "
                f"Todėl kai {self.source} sako, kad {self.target} yra riteris, žinome, kad "
                f"{self.target} ir {self.source} yra to paties tipo. "
                f"Kadangi {known} yra {known.type()}, tada {unknown} yra {unknown.type()}."
            )
        return (
            "All islanders will call one of their same kind a knight. "
            f"So when {self.source} says that {self.target} is a knight, we know that "
            f"{self.target} and {self.source} are the same type. "
            f"Since {known} is a {known.type()}, then {unknown} is a {unknown.type()}."
        )


class Sympathetic(Statement):
    def build_statement(self) -> str:
        if ACTIVE_LANGUAGE == "lt":
            return self.target.name + " yra tokio pat tipo kaip aš"
        return self.target.name + " is my type"

    def reasoning(self) -> str:
        if ACTIVE_LANGUAGE == "lt":
            return (
                "Ir riteris, ir melagis sakys, kad jie yra tokio pat tipo kaip riteris. "
                f"Todėl kai {self.source} sako, kad yra tokio pat tipo kaip {self.target}, "
                f"žinome, kad {self.target} yra riteris."
            )
        return (
            "A knight or a knave will say they are the same type as a knight. "
            f"So when {self.source} says they are the same type as {self.target}, "
            f"we know that {self.target} is a knight."
        )

    def solve(self, solver: "Solver"):
        solver.reasoning.append(self.reasoning())
        add_unique(solver.knights, self.target)


class Antithetic(Statement):
    def build_statement(self) -> str:
        if ACTIVE_LANGUAGE == "lt":
            return self.target.name + " nėra tokio pat tipo kaip aš"
        return self.target.name + " is not my type"

    def reasoning(self) -> str:
        if ACTIVE_LANGUAGE == "lt":
            return (
                "Tiek riteriai, tiek melagiai sakys, kad jie nėra tokio pat tipo kaip melagis. "
                f"Todėl kai {self.source} sako, kad yra kitokio tipo nei {self.target}, "
                f"žinome, kad {self.target} yra melagis."
            )
        return (
            "Both knights and knaves will say they are not the same type as a knave. "
            f"So when {self.source} says they are a different type than {self.target}, "
            f"we know that {self.target} is a knave."
        )

    def solve(self, solver: "Solver"):
        solver.reasoning.append(self.reasoning())
        add_unique(solver.knaves, self.target)


class Disjoint(Statement):
    def build_statement(self) -> str:
        txt = self.target.name
        if ACTIVE_LANGUAGE == "lt":
            txt += " yra riteris " if self.target.is_knight() else " yra melagis "
            return txt + "arba aš esu melagis"
        txt += " is a knight " if self.target.is_knight() else " is a knave "
        return txt + "or I am a knave"

    def reasoning(self) -> str:
        if ACTIVE_LANGUAGE == "lt":
            return (
                f"Kai {self.source} pasakė '{self.text},' žinome, kad {self.source} būtinai sako tiesą. "
                "(Jei tai būtų netiesa, kalbėtojas būtų melagis, o tai paverstų teiginį tiesa, "
                "tačiau melagiai negali sakyti tiesos.) "
                f"Todėl {self.source} yra riteris ir {self.target} yra {self.target.type()}."
            )
        return (
            f"When {self.source} said '{self.text},' we know {self.source} must be making a true statement. "
            "(If it was false, this would make the speaker a knave, which would make the statement true, "
            "but knaves cannot make true statements.) "
            f"So, {self.source} is a knight and {self.target} is a {self.target.type()}."
        )

    def solve(self, solver: "Solver"):
        solver.reasoning.append(self.reasoning())
        add_unique(solver.knights, self.source)
        if self.target.is_knight():
            add_unique(solver.knights, self.target)
        else:
            add_unique(solver.knaves, self.target)


class Joint(Statement):
    def build_statement(self) -> str:
        txt = self.target.name
        if ACTIVE_LANGUAGE == "lt":
            txt += " yra melagis " if self.target.is_knight() else " yra riteris "
            return txt + "ir aš esu melagis"
        txt += " is a knave " if self.target.is_knight() else " is a knight "
        return txt + "and I am a knave"

    def reasoning(self) -> str:
        if ACTIVE_LANGUAGE == "lt":
            return (
                f"Kadangi {self.source} pasakė '{self.text},' žinome, kad {self.source} nesako tiesos. "
                "(Jei tai būtų tiesa, kalbėtojas būtų riteris, teigiantis, kad yra melagis, o taip negali būti.) "
                f"Todėl {self.source} yra melagis ir {self.target} yra {self.target.type()}."
            )
        return (
            f"Because {self.source} said '{self.text},' we know {self.source} is not making a true statement. "
            "(If it was true, the speaker would be a knight claiming to be a knave, which cannot happen.) "
            f"Therefore, {self.source} is a knave and {self.target} is a {self.target.type()}."
        )

    def solve(self, solver: "Solver"):
        solver.reasoning.append(self.reasoning())
        add_unique(solver.knaves, self.source)
        if self.target.is_knight():
            add_unique(solver.knights, self.target)
        else:
            add_unique(solver.knaves, self.target)


def all_sources_and_targets(islander: Islander, statements: List[TypeStatement]):
    out = [islander]
    for st in statements:
        if islander is st.source:
            out.append(st.target)
        if islander is st.target:
            out.append(st.source)
    return out


def all_reachable(islander: Islander, statements: List[TypeStatement], so_far: List[Islander]):
    reachable = so_far.copy()
    immediate = all_sources_and_targets(islander, statements)
    reachable = add_all_unique(reachable, immediate)
    if arrays_equivalent(reachable, so_far):
        return so_far
    for node in immediate:
        add_all_unique(reachable, all_reachable(node, statements, reachable))
    return reachable


def connected_sets(
    islanders: List[Islander],
    complete_islanders: List[Islander],
    statements: List[TypeStatement],
    set_list: List[List[Islander]],
    so_far: List[Islander],
):
    connect_1 = all_reachable(islanders[0], statements, [])
    add_all_unique(so_far, connect_1)
    set_list.append(connect_1)
    if arrays_equivalent(complete_islanders, so_far):
        return set_list
    remainder = array_difference(islanders, so_far)
    return connected_sets(remainder, complete_islanders, statements, set_list, so_far)


def join_connected_sets(islanders: List[Islander], statements: List[TypeStatement]):
    c_sets = connected_sets(islanders, islanders, statements, [], [])
    if len(c_sets) == 1:
        return statements
    joiner = c_sets[0][0]
    remaining_sets = remove_element(c_sets, c_sets[0])
    new_statements = []
    for set_ in remaining_sets:
        joinee = set_[0]
        new_statements.append(joinee.statement_for(joiner))
    return statements + new_statements


def prune_statements(statements: List[TypeStatement]):
    extras = []
    for e in statements:
        if array_contains(extras, e):
            continue
        s, t = e.source, e.target
        remainder = array_without_element(statements, e)
        for e1 in remainder:
            if e1.source is t and e1.target is s:
                extras.append(e1)
    return array_difference(statements, extras)


def remove_statement_with(islander_1: Islander, islander_2: Islander, statements: List[TypeStatement]):
    for e in statements:
        s, t = e.source, e.target
        if (s is islander_1 or s is islander_2) and (t is islander_1 or t is islander_2):
            return array_without_element(statements, e)
    return statements


class Puzzle:
    def __init__(self):
        self.islanders: List[Islander] = []
        self.statements: List[Statement] = []
        self.knaves: List[Knave] = []
        self.knights: List[Knight] = []

    def knave_names(self) -> List[str]:
        return [k.name for k in self.knaves]

    def knight_names(self) -> List[str]:
        return [k.name for k in self.knights]


class CompoundPuzzle(Puzzle):
    def __init__(self):
        super().__init__()
        self.puzzles: List[Puzzle] = []

    def join(self, target: Puzzle):
        self.puzzles.append(target)
        self.knaves = add_all_unique(self.knaves, target.knaves)
        self.knights = add_all_unique(self.knights, target.knights)
        self.islanders = add_all_unique(self.islanders, target.islanders)
        self.statements = add_all_unique(self.statements, target.statements)

    def random_join(self, target: Puzzle):
        if random_int(2) == 0:
            self.join_with_match(target)
        else:
            self.join_with_compound(target)

    def join_with_match(self, target: Puzzle):
        s = random_element(self.islanders)
        t = random_element(target.islanders)
        self.join(target)
        self.statements.append(s.match_statement_for(t))

    def join_with_compound(self, target: Puzzle):
        s = random_element(self.islanders)
        t = random_element(target.islanders)
        self.join(target)
        self.statements.append(s.compound_statement_for(t))


class SimplePuzzle(Puzzle):
    def __init__(self, count: int, names: Optional[List[str]] = None):
        super().__init__()
        self.count = count
        if count == 1:
            self.liar_count = 1
        elif count < 4:
            self.liar_count = random_int(count)
        else:
            self.liar_count = random_range((count // 2) - 1, count - 2)
        self.name_set = names if names is not None else ORIGINAL_NAME_SET.copy()

        for _ in range(self.liar_count):
            pos = random_range(0, len(self.name_set) - 1)
            islander = Knave(self.name_set.pop(pos))
            self.knaves.append(islander)

        for _ in range(self.liar_count, self.count):
            pos = random_range(0, len(self.name_set) - 1)
            islander = Knight(self.name_set.pop(pos))
            self.knights.append(islander)

        self.islanders = shuffle(self.knaves + self.knights)
        self.statements = self.generate_statements()

    def generate_statements(self) -> List[TypeStatement]:
        statements: List[TypeStatement] = []
        if len(self.islanders) < 2:
            return statements

        prev_source = None
        for target in self.islanders:
            remainders = array_without_element(self.islanders, target)
            if prev_source is not None:
                remainders = array_without_element(remainders, prev_source)
                if len(remainders) == 0:
                    remainders = array_without_element(self.islanders, target)
            source = random_element(remainders)
            statements.append(source.statement_for(target))
            prev_source = source

        statements = prune_statements(statements)
        statements = join_connected_sets(self.islanders, statements)
        return shuffle(statements)

    def complete_with_match(self):
        if len(self.islanders) < 2:
            return
        source = random_element(self.islanders)
        remainders = array_without_element(self.islanders, source)
        neighbors = all_sources_and_targets(source, self.statements)
        left = array_difference(remainders, neighbors)
        target = random_element(left) if len(left) > 0 else random_element(remainders)
        self.statements.append(source.match_statement_for(target))
        shuffle(self.statements)

    def complete_with_compound(self):
        if len(self.islanders) < 2:
            return
        source = random_element(self.islanders)
        remainders = array_without_element(self.islanders, source)
        neighbors = all_sources_and_targets(source, self.statements)
        left = array_difference(remainders, neighbors)
        target = random_element(left) if len(left) > 0 else random_element(remainders)
        self.statements = remove_statement_with(source, target, self.statements)
        self.statements.append(source.compound_statement_for(target))
        shuffle(self.statements)

    def random_completion(self):
        if random_int(2) == 0:
            self.complete_with_match()
        else:
            self.complete_with_compound()


class Solver:
    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle
        self.reasoning: List[str] = []
        self.type_statements: List[TypeStatement] = []
        self.knights: List[Knight] = []
        self.knaves: List[Knave] = []

    def solve(self) -> str:
        for statement in self.puzzle.statements:
            statement.solve(self)

        remaining = self.type_statements.copy()
        while len(remaining) != 0:
            next_remaining = remaining.copy()
            for s in remaining:
                if s.done(self):
                    next_remaining = remove_element(next_remaining, s)
                    continue
                knave_copy = self.knaves.copy()
                for k in knave_copy:
                    s.process(k, self)
                if s.done(self):
                    next_remaining = remove_element(next_remaining, s)
                    continue
                knight_copy = self.knights.copy()
                for k in knight_copy:
                    s.process(k, self)
            remaining = next_remaining

        lines = [f"{r}" for r in self.reasoning]
        summary = "\n".join(lines)
        summary += "\n" + text("for_these_reasons")
        if len(self.puzzle.knave_names()) == 0:
            summary += text("no_knaves")
        elif len(self.puzzle.knave_names()) == 1:
            summary += f"{text('only_knave')}{pretty_print_list(self.puzzle.knave_names())}"
        else:
            summary += f"{text('knaves_were')}{pretty_print_list(self.puzzle.knave_names())}"
        if len(self.puzzle.knight_names()) == 0:
            summary += text("and_no_knights")
        elif len(self.puzzle.knight_names()) == 1:
            summary += f"{text('and_only_knight')}{pretty_print_list(self.puzzle.knight_names())}."
        else:
            summary += f"{text('and_knights_were')}{pretty_print_list(self.puzzle.knight_names())}."
        return summary


class PuzzleGenerator:
    def __init__(self):
        self.puzzle: Optional[Puzzle] = None

    def easy(self):
        choice = random_int(3)
        if choice == 0:
            self.easy0()
        elif choice == 1:
            self.easy1()
        else:
            self.easy2()

    def medium(self):
        choice = random_int(3)
        if choice == 0:
            self.medium0()
        elif choice == 1:
            self.medium1()
        else:
            self.medium2()

    def hard(self):
        choice = random_int(2)
        if choice == 0:
            self.hard0()
        else:
            self.hard1()

    def easy0(self):
        self.puzzle = SimplePuzzle(2, name_set())
        self.puzzle.complete_with_match()
        return self.puzzle

    def easy1(self):
        self.puzzle = SimplePuzzle(2, name_set())
        self.puzzle.complete_with_compound()
        return self.puzzle

    def easy2(self):
        self.puzzle = SimplePuzzle(3, name_set())
        self.puzzle.random_completion()
        return self.puzzle

    def medium0(self):
        names = name_set()
        basic = SimplePuzzle(3, names)
        basic1 = SimplePuzzle(1, names)
        basic.random_completion()
        self.puzzle = CompoundPuzzle()
        self.puzzle.join(basic)
        self.puzzle.random_join(basic1)
        return self.puzzle

    def medium1(self):
        names = name_set()
        basic = SimplePuzzle(3, names)
        basic.complete_with_match()
        self.puzzle = CompoundPuzzle()
        self.puzzle.join(basic)
        return self.puzzle

    def medium2(self):
        names = name_set()
        basic = SimplePuzzle(1, names)
        basic1 = SimplePuzzle(3, names)
        self.puzzle = CompoundPuzzle()
        self.puzzle.join(basic)
        self.puzzle.join_with_compound(basic1)
        return self.puzzle

    def hard0(self):
        names = name_set()
        basic = SimplePuzzle(3, names)
        basic2 = SimplePuzzle(3, names)
        self.puzzle = CompoundPuzzle()
        self.puzzle.join(basic)
        self.puzzle.join_with_compound(basic2)
        return self.puzzle

    def hard1(self):
        names = name_set()
        basic = SimplePuzzle(3, names)
        basic2 = SimplePuzzle(3, names)
        basic.complete_with_match()
        self.puzzle = CompoundPuzzle()
        self.puzzle.join(basic)
        self.puzzle.join_with_match(basic2)
        return self.puzzle

    def solution_summary(self, knaves_list: List[str], knights_list: List[str]) -> str:
        result = sorted(knaves_list) == sorted(self.puzzle.knave_names())
        result = result and (sorted(knights_list) == sorted(self.puzzle.knight_names()))

        if len(knaves_list) == 0:
            s = text("you_said_no_knaves")
        elif len(knaves_list) == 1:
            s = f"{text('you_said_one_knave')}{pretty_print_list(knaves_list)},"
        else:
            s = f"{text('you_said_knaves')}{pretty_print_list(knaves_list)},"

        if len(knights_list) == 0:
            s += text("and_that_no_knights")
        elif len(knights_list) == 1:
            s += f"{text('and_that_one_knight')}{pretty_print_list(knights_list)}."
        else:
            s += f"{text('and_that_knights')}{pretty_print_list(knights_list)}."

        if result:
            s += text("you_were_right")
        else:
            s += text("you_were_wrong")
            if len(self.puzzle.knave_names()) == 0:
                s += text("there_were_no_knaves")
            elif len(self.puzzle.knave_names()) == 1:
                s += f"{text('the_only_knave')}{pretty_print_list(self.puzzle.knave_names())}"
            else:
                s += f"{text('the_knaves_were')}{pretty_print_list(self.puzzle.knave_names())}"

            if len(self.puzzle.knight_names()) == 0:
                s += text("and_no_knights")
            elif len(self.puzzle.knight_names()) == 1:
                s += f"{text('and_only_knight')}{pretty_print_list(self.puzzle.knight_names())}."
            else:
                s += f"{text('and_knights_were')}{pretty_print_list(self.puzzle.knight_names())}."

        return s

    def show_reasoning(self) -> str:
        solver = Solver(self.puzzle)
        return solver.solve()


@dataclass
class DifficultyPlan:
    label: str
    method: str
    count: int


def generate_one(difficulty_label: str, method_name: str, idx: int, system_prompt: str = ""):
    pg = PuzzleGenerator()
    getattr(pg, method_name)()
    puzzle = pg.puzzle
    knaves = puzzle.knave_names()
    knights = puzzle.knight_names()
    islanders = [i.name for i in puzzle.islanders]
    statements = [s.full_statement() for s in puzzle.statements]
    prompt = build_prompt(islanders, statements)

    return {
        "id": idx,
        "difficulty": map_difficulty_label(difficulty_label),
        "islanders": islanders,
        "statements": statements,
        "answer": {"knaves": knaves, "knights": knights},
        "answer_text": pg.solution_summary(knaves, knights),
        "reasoning_text": pg.show_reasoning(),
        "prompt": prompt,
        "system_prompt": system_prompt,
    }


def generate_dataset(plans: List[DifficultyPlan], system_prompt: str = ""):
    rows = []
    idx = 1
    for plan in plans:
        for _ in range(plan.count):
            rows.append(generate_one(plan.label, plan.method, idx, system_prompt))
            idx += 1
    return rows


def write_jsonl(path: str, rows: List[dict]):
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def parse_args():
    parser = argparse.ArgumentParser(description="Generate knaves dataset in JSONL format.")
    parser.add_argument("--easy", type=int, default=40, help="Number of easy puzzles.")
    parser.add_argument("--medium", type=int, default=40, help="Number of medium puzzles.")
    parser.add_argument("--hard", type=int, default=20, help="Number of hard puzzles.")
    parser.add_argument("--seed", type=int, default=None, help="Optional random seed for reproducibility.")
    parser.add_argument("--language", type=str, default="lt", choices=["en", "lt"], help="Dataset language.")
    parser.add_argument(
        "--output",
        type=str,
        default="riteriu_dataset/out/riteriai_dataset_40_40_20.jsonl",
        help="Output JSONL path.",
    )
    parser.add_argument(
        "--system-prompt-file",
        type=str,
        default="riteriu_dataset/system_prompts/system_prompt_lt.txt",
        help="Optional .txt file path for system prompt to include in each row.",
    )
    return parser.parse_args()


def read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    global ACTIVE_LANGUAGE
    args = parse_args()
    ACTIVE_LANGUAGE = args.language
    if args.seed is not None:
        random.seed(args.seed)

    system_prompt = ""
    if args.system_prompt_file:
        system_prompt = read_text_file(args.system_prompt_file)

    plans = [
        DifficultyPlan("easy", "easy", args.easy),
        DifficultyPlan("medium", "medium", args.medium),
        DifficultyPlan("hard", "hard", args.hard),
    ]
    rows = generate_dataset(plans, system_prompt)
    write_jsonl(args.output, rows)
    print(f"Wrote {len(rows)} puzzles to {args.output}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
# Author: Tiancheng Zhao
# Date: 9/13/17

import numpy as np
from simdial.agent.core import SystemAct, UserAct, BaseUsrSlot
from simdial.agent import core
import json
import copy


class AbstractNlg(object):
    """
    Abstract class of NLG
    """

    def __init__(self, domain, complexity):
        self.domain = domain
        self.complexity = complexity

    def generate_sent(self, actions, **kwargs):
        """
        Map a list of actions to a string.

        :param actions: a list of actions
        :return: uttearnces in string
        """
        raise NotImplementedError("Generate sent is required for NLG")

    def sample(self, examples):
        return np.random.choice(examples)


class SysCommonNlg(object):
    templates = {SystemAct.GREET: ["挨拶"],
                 SystemAct.ASK_REPEAT: ["ああああああああ"],
                 SystemAct.ASK_REPHRASE: ["別の言い方で言って下さい。"],
                 SystemAct.GOODBYE: ["さようなら。"],
                 SystemAct.CLARIFY: ["わかりません。"],
                 SystemAct.REQUEST+core.BaseUsrSlot.NEED: ["レストランの検索ができます。"],
                 SystemAct.REQUEST+core.BaseUsrSlot.HAPPY: ["他には何かありますか？",
                                                            "他にも何でも聞いて下さい。",
                                                            "それ以外に手伝えることはありますか？"],
                 SystemAct.EXPLICIT_CONFIRM+"dont_care": ["気にしない、ということですね？",
                                                          "気にしないのであっていますか？"],
                 SystemAct.IMPLICIT_CONFIRM+"dont_care": ["気にしない、ということですね。",
                                                          "分かりました。"]}

class SysNlg(AbstractNlg):
    """
    NLG class to generate utterances for the system side.
    """

    def generate_sent(self, actions, domain=None, templates=SysCommonNlg.templates):
        """
         Map a list of system actions to a string.

        :param actions: a list of actions
        :param templates: a common NLG template that uses the default one if not given
        :return: uttearnces in string
        """
        str_actions = []
        lexicalized_actions = []
        for a in actions:
            a_copy = copy.deepcopy(a)
            if a.act == SystemAct.GREET:
                if domain:
                    str_actions.append(domain.greet)
                else:
                    str_actions.append(self.sample(templates[a.act]))

            elif a.act == SystemAct.QUERY:
                usr_constrains = a.parameters[0]
                sys_goals = a.parameters[1]

                # create string list for KB_SEARCH
                search_dict = {}
                for k, v in usr_constrains:
                    slot = self.domain.get_usr_slot(k)
                    if v is None:
                        search_dict[k] = 'dont_care'
                    else:
                        search_dict[k] = slot.vocabulary[v]

                a_copy.parameters[0] = search_dict
                a_copy.parameters[1] = sys_goals
                str_actions.append(json.dumps({"QUERY": search_dict,
                                               "GOALS": sys_goals}))

            elif a.act == SystemAct.INFORM:
                sys_goals = a.parameters[1]

                # create string list for RET + Informs
                informs = []
                sys_goal_dict = {}
                for k, (v, e_v) in sys_goals.items():
                    slot = self.domain.get_sys_slot(k)
                    sys_goal_dict[k] = slot.vocabulary[v]

                    if e_v is not None:
                        prefix = "Yes, " if v == e_v else "No, "
                    else:
                        prefix = ""
                    informs.append(prefix + slot.sample_inform()
                                   % slot.vocabulary[v])
                a_copy['parameters'] = [sys_goal_dict]
                str_actions.append(" ".join(informs))

            elif a.act == SystemAct.REQUEST:
                slot_type, _ = a.parameters[0]
                if slot_type in [core.BaseUsrSlot.NEED, core.BaseUsrSlot.HAPPY]:
                    str_actions.append(self.sample(templates[SystemAct.REQUEST+slot_type]))
                else:
                    target_slot = self.domain.get_usr_slot(slot_type)
                    if target_slot is None:
                        raise ValueError("none slot %s" % slot_type)
                    str_actions.append(target_slot.sample_request())

            elif a.act == SystemAct.EXPLICIT_CONFIRM:
                slot_type, slot_val = a.parameters[0]
                if slot_val is None:
                    str_actions.append(self.sample(templates[SystemAct.EXPLICIT_CONFIRM+"dont_care"]))
                    a_copy.parameters[0] = (slot_type, "dont_care")
                else:
                    slot = self.domain.get_usr_slot(slot_type)
                    str_actions.append("Do you mean %s?"
                                       % slot.vocabulary[slot_val])
                    a_copy.parameters[0] = (slot_type, slot.vocabulary[slot_val])

            elif a.act == SystemAct.IMPLICIT_CONFIRM:
                slot_type, slot_val = a.parameters[0]
                if slot_val is None:
                    str_actions.append(self.sample(templates[SystemAct.IMPLICIT_CONFIRM+"dont_care"]))
                    a_copy.parameters[0] = (slot_type, "dont_care")
                else:
                    slot = self.domain.get_usr_slot(slot_type)
                    str_actions.append("I believe you said %s."
                                       % slot.vocabulary[slot_val])
                    a_copy.parameters[0] = (slot_type, slot.vocabulary[slot_val])

            elif a.act in templates.keys():
                str_actions.append(self.sample(templates[a.act]))

            else:
                raise ValueError("Unknown dialog act %s" % a.act)

            lexicalized_actions.append(a_copy)

        return " ".join(str_actions), lexicalized_actions


class UserNlg(AbstractNlg):
    """
    NLG class to generate utterances for the user side.
    """

    def generate_sent(self, actions):
        """
         Map a list of user actions to a string.

        :param actions: a list of actions
        :return: uttearnces in string
        """
        str_actions = []
        for a in actions:
            if a.act == UserAct.KB_RETURN:
                sys_goals = a.parameters[1]
                sys_goal_dict = {}
                for k, v in sys_goals.items():
                    slot = self.domain.get_sys_slot(k)
                    sys_goal_dict[k] = slot.vocabulary[v]

                str_actions.append(json.dumps({"RET": sys_goal_dict}))
            elif a.act == UserAct.GREET:
                str_actions.append(self.sample(["挨拶"]))

            elif a.act == UserAct.GOODBYE:
                str_actions.append(self.sample(["大丈夫です。"]))

            elif a.act == UserAct.REQUEST:
                slot_type, _ = a.parameters[0]
                target_slot = self.domain.get_sys_slot(slot_type)
                str_actions.append(target_slot.sample_request())

            elif a.act == UserAct.INFORM:
                has_self_correct = a.parameters[-1][0] == BaseUsrSlot.SELF_CORRECT
                slot_type, slot_value = a.parameters[0]
                target_slot = self.domain.get_usr_slot(slot_type)

                def get_inform_utt(val):
                    if val is None:
                        return self.sample(["何でも大丈夫です。", "特に気にしません。"])
                    else:
                        return target_slot.sample_inform() % target_slot.vocabulary[val]

                if has_self_correct:
                    wrong_value = target_slot.sample_different(slot_value)
                    wrong_utt = get_inform_utt(wrong_value)
                    correct_utt = get_inform_utt(slot_value)
                    connector = self.sample(["Oh no,", "Uhm sorry,", "Oh sorry,"])
                    str_actions.append("%s %s %s" % (wrong_utt, connector, correct_utt))
                else:
                    str_actions.append(get_inform_utt(slot_value))

            elif a.act == UserAct.CHAT:
                str_actions.append(self.sample(["What's your name?", "Where are you from?"]))

            elif a.act == UserAct.YN_QUESTION:
                slot_type, expect_id = a.parameters[0]
                target_slot = self.domain.get_sys_slot(slot_type)
                expect_val = target_slot.vocabulary[expect_id]
                str_actions.append(target_slot.sample_yn_question(expect_val))

            elif a.act == UserAct.CONFIRM:
                str_actions.append(self.sample(["はい", "そうです", "それで合っています", "うん", "ok"]))

            elif a.act == UserAct.DISCONFIRM:
                str_actions.append(self.sample(["そうじゃない", "いいえ", "ちゃう", "違います", "ちがう"]))

            elif a.act == UserAct.SATISFY:
                str_actions.append(self.sample(["大丈夫です。", "十分です", "もういい"]))

            elif a.act == UserAct.MORE_REQUEST:
                str_actions.append(self.sample(["他にもあります。", "聞きたいことがあります。", "まだ"]))

            elif a.act == UserAct.NEW_SEARCH:
                str_actions.append(self.sample(["別に探して欲しい", "新しい条件で探して", "新しい検索条件"]))

            else:
                raise ValueError("Unknown user act %s for NLG" % a.act)

        return " ".join(str_actions)

    def add_hesitation(self, sents, actions):
        pass

    def add_self_restart(self, sents, actions):
        pass

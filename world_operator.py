from Blocks_World import *

class WorldOperator:
    def __init__(self, data):
        """
        :param data: a Data object
        :return: None
        """
        self.db = data

    def execute(self, command, args):
        """
        Commands:                                   Example command:
            -create_block                               "a is a block."
            -create_type                                "blue is a type."
            -instance_type_query                        "is a blue?"
            -type_type_query                            "are all blocks that are magenta red?"
            -set_instance_type                          "a is blue."
            -set_type_implication                       "all blocks that are magenta are red."
            -set_on_set                                 "on(a,B), on(B,fasd)."
            -display_data                               "list data."
            -what_is_on                                 "what is a on?"
            -is_on                                      "is a on b?"


        :param command: command to execute
        :param args: arguments to that command
        :return: string indicating the result of the (attempted) execution of command over args
        """
        if command is 'create_block' and len(args) == 1:
            return self.create_block(args[0])
        elif command is 'create_type' and len(args) == 1:
            return self.create_type(args[0])
        if command is 'set_instance_type' and len(args) == 2:
            return self.set_instance_type(args[0], args[1])
        elif command is 'set_type_implication' and len(args) == 2:
            return self.set_type_implication(args[0], args[1])
        elif command is 'instance_type_query' and len(args) == 2:
            return self.instance_type_query(args[0], args[1])
        elif command is 'type_type_query' and len(args) == 2:
            return self.type_type_query(args[0], args[1])
        elif command is 'display_data' and len(args) == 0:
            return self.display_data()
        elif command is 'set_on_set' and len(args) % 2 == 0:
            return self.set_on_set(args)
        elif command is 'what_is_on' and len(args) == 1:
            return self.what_is_on(args[0])
        elif command is 'is_on' and len(args) == 2:
            return self.is_on(args[0], args[1])
        else:
            raise Exception('Unrecognized command: %s with %s arguments' % (command, str(len(args))))

    def create_block(self, block_name):
        """
        Creates block block_name, if it doesn't already exist
        :param block_name: name of block
        :return: String indicating success/failure of block creation.
            The returned string should be of one of the following forms (block_name = "A"):
                "Block A already exists"
                "OK, created block A"
        """
        if self.db.check_block(block_name):
            return 'Block %s already exists' % block_name
        else:
            self.db.add_block(block_name)
            self.db.set_on(block_name, 'table')
            return 'OK, created block %s' % block_name

    def create_type(self, type_name):
        """
        Creates a type type_name, if it doesn't already exist
        :param type_name: name of the type
        :return: String indicating success/failure of type creation.
            The returned string should be of one of the following forms (type_name = "blue"):
                "Type blue already exists"
                "OK, created type blue"
        """
        if self.db.check_type(type_name):
            return 'Type %s already exists' % type_name
        else:
            self.db.add_type(type_name)
            return 'OK, created type %s' % type_name

    def set_instance_type(self, block, type):
        """
        Sets block to be of type type. If there is no such block, this is indicated. If there is such a block,
        but no such type, this is indicated.
        :param block: block name
        :param type: type name
        :return: String indicating success/failure of assigning block to be of type type
            The returned string should be of one of the following forms (block = "A", type = "blue"):
                "No such block: A"
                "No such type: blue"
                "OK, A is now blue"
        """
        if not self.db.check_block(block):
            return 'No such block: %s' % block
        elif not self.db.check_type(type):
            return 'No such type: %s' % type
        else:
            self.db.set_block_type(block, type)
            return 'OK, %s is now %s' % (block, type)

    def set_type_implication(self, type_one, type_two):
        """
        Sets all current block of type_one to also be of type_two. If the first type does not exist, this is indicated.
        If the first type exists, but the second does not, this is indicated.
        :param type_one: name of first type
        :param type_two: name of second type
        :return: String indicating success/failure of assigning type_two to all current blocks of type_one
            The returned string should be of one of the following forms (type_one = "blue", type_two = "green"):
                "No such type: blue"
                "No such type: green"
                "OK, all blocks that are blue are now green"
        """
        if not self.db.check_type(type_one):
            return 'No such type: %s' % type_one
        elif not self.db.check_type(type_two):
            return 'No such type: %s' % type_two
        else:
            for block in self.db.list_blocks():
                if self.db.check_block_type(block, type_one):
                    self.db.set_block_type(block, type_two)
        return 'OK, all blocks that are %s are now %s' % (type_one, type_two)

    def instance_type_query(self, block, type):
        """
        Determines whether block is of type type. If block does not exist, this is indicated. If block exists, but
        type does not exist, this is indicated.
        :param block: name of block
        :param type: name of type
        :return: String indicating whether block is of type type.
            The returned string should be of one of the following forms (block = "A", type = "blue"):
                "No such block: A"
                "No such type: blue"
                "Yes, A is blue"
                "No, a is not blue"
        """
        if not self.db.check_block(block):
            return 'No such block: %s' % block
        elif not self.db.check_type(type):
            return 'No such type: %s' % type
        else:
            if self.db.check_block_type(block, type):
                return 'Yes, %s is %s' % (block, type)
            else:
                return 'No, %s is not %s' % (block, type)

    def type_type_query(self, type_one, type_two):
        """
        Determines whether all current blocks of type_one are also of type_two. If type_one does not exist, this is
        indicated. If type_one exists, but type_two does not, this is indicated.
        :param type_one: the first type
        :param type_two: the second type
        :return: String indicating whether all blocks of type_one are also of type_two.
            The returned string should be of one of the following forms (type_one = "blue", type_two = "green"):
                "No such type: blue"
                "No such type: green"
                "No, not all blocks that are blue are green"
                "Yes, all blocks that are blue are green"
        """
        if not self.db.check_type(type_one):
            return 'No such type: %s' % type_one
        elif not self.db.check_type(type_two):
            return 'No such type: %s' % type_two
        else:
            for block in self.db.list_blocks():
                if self.db.check_block_type(block, type_one) and not self.db.check_block_type(block, type_two):
                    return 'No, not all blocks that are %s are %s' % (type_one, type_two)
            return 'Yes, all blocks that are %s are %s' % (type_one, type_two)

    def display_data(self):
        """
        Provides information of all current data.
        :return: String representing all current data.
        """
        return self.db.display_data()

    def set_on_set(self, args):
        """
        Given a series of blocks, of odd length, places each block of even index i, args[i], onto block args[i+1].
        If any block does not exist, the non-existence of the first non-existent block is indicated.
        :param args: array, of odd length, containing blocks to stack
        :return: String containing the plan, as produced by an HTN, If no such plan exists, this is indicated.
            The returned string should be of one of the following forms (args = ['a', 'b', 'b', 'c'], where
            all of a, b, and c are presently on the table):

            "
            HTN Actions:
            1.  ('pickup', 'b')
            2.  ('stack', 'b', 'c')
            3.  ('pickup', 'a')
            4.  ('stack', 'a', 'b')
            Actions executed.
            "

            "Plan cannot be formulated"
        """

        sstate = State('Start state')
        gstate = State('Goal state')

        sstate.holding = False
        gstate.holding = False

        sstate.pos = {}
        gstate.pos = {}

        for on in self.db.list_on():
            sstate.pos[on[0]] = on[1]
            gstate.pos[on[0]] = on[1]

        for i in range(0, len(args), 2):
            gstate.pos[args[i]] = args[i+1]

        HTNplanner = HTNPlanner("Blocks_World")
        HTNplanner.declare_operators(pickup, unstack, putdown, stack)
        HTNplanner.declare_methods('put', put_m)
        HTNplanner.declare_methods('get', get_m)
        HTNplanner.declare_methods('move_one', move1)
        HTNplanner.declare_methods('move_blocks', moveb_m)
        HTNplanner.planner(sstate, [('move_blocks', gstate)])
        plan = [p for p in HTNplanner.planningsteps.items() if p[1][0] == 'operator']
        print("HTN Actions:")
        for cnt, elem in enumerate(plan):
            print("%s.  %s " % (cnt + 1, elem[1][1]))

        return 'TODO: EXECUTE PLAN'     ####################################################### TODO: execute plan

    def what_is_on(self, block):
        """
        Determines what block is on, if anything.
        :param block: the name of the block
        :return: String indicating what block is on.
            The returned string should be of one of the following forms (block = "A"):
                "No such block: A"
                "A is on table"                 (if A is on table)
                "A is on B"                     (if A is on B)
                "A is not on anything"          (if A is not on anything)
        """
        if not self.db.check_block(block):
            return 'No such block: %s' % block

        for on in self.db.list_on():
            if on[0] == block:
                return 'Block %s is on block %s' % (block, on[1])

        return 'Block %s is not on anything' % block


    def is_on(self, block_a, block_b):
        """
        Determines whether block_a is on block_b
        :param block_a: name of block_a
        :param block_b: name of block_b
        :return: String indicating whether block_a is on block_b. If there is no such block block_a, this is indicated.
        If block_a exists, but there is no such block block_b, this is indicated.
            The returned string should be of one of the following forms (block_a = "A", block_b = "B"):
                "No such block: A"
                "No such block: B"
                "Yes, block A is on block B"
                "No, block A is not on block B"
        """

        if not self.db.check_block(block_a):
            return 'No such block: %s' % block_a

        if not self.db.check_block(block_b):
            return 'No such block: %s' % block_b

        for on in self.db.list_on():
            if on[0] == block_a and on[1] == block_b:
                return 'Yes, block %s is on block %s' % (block_a, block_b)

        return 'No, block %s is not on block %s' % (block_a, block_b)


import sqlite3 as lite
import os

class Data:
    """
    Manages a database holding blocks and their properties and relations.
    """
    def __init__(self, database, wipe=True):
        """
        if wipe == False:
            opens database
        else:
            Creates a database in file database, and initializes all tables and the 'on' relation
        :param database: Filename of the database
        :param wipe: Whether to clear the contents of the database
        :return:
        """
        if wipe:
            try:
                os.remove(database)
            except Exception as e:
                print(e)

        self.db = lite.connect(database)
        self.cursor = self.db.cursor()

        if wipe:
            self.cursor.execute('CREATE TABLE instance(name TEXT, block INTEGER DEFAULT 1)')            # Contains each block. First column is name, other columns are type membership. Every block is a block
            self.cursor.execute('CREATE TABLE on_relation(top TEXT, bottom TEXT)')                      # Block A is on Block B

            self.cursor.execute("INSERT INTO instance(name) VALUES('table')")

            self.db.commit()

    def list_blocks(self):
        """
        :return: a list of block names
        """
        self.cursor.execute('SELECT name FROM instance')
        instances = [f[0] for f in self.cursor.fetchall()]

        return instances

    def check_block(self, block_name):
        """
        :param block_name: name of block
        :return: True if block exists, False otherwise
        """
        self.cursor.execute('SELECT name FROM instance')
        instances = [f[0] for f in self.cursor.fetchall()]

        return block_name in instances

    def check_type(self, type_name):
        """
        :param type_name: name of type to check
        :return: True if type_name is already a type, False otherwise
        """
        self.cursor.execute("SELECT * FROM instance")
        types = [f[0] for f in self.cursor.description][1:]
        return type_name in types

    def add_block(self, block_name):
        """
        Adds block_name to the database with default values for all type membership.
        :param block_name: String: name of block to add
        :return: None
        """
        assert not self.check_block(block_name), 'Block already exists: %s' % block_name                # If block already exists, then crash

        self.cursor.execute("INSERT INTO instance(name) VALUES('%s')" % block_name)                     # Default values for everything but name
        self.db.commit()

    def add_type(self, type_name):
        """
        Add a type to the database. No instances will be of this type until set to this type.
        :param typename:
        :return: None
        """
        self.cursor.execute('ALTER TABLE instance ADD COLUMN %s INTEGER DEFAULT 0' % type_name)
        self.db.commit()

    def list_on(self):
        self.cursor.execute('SELECT * FROM on_relation')
        return self.cursor.fetchall()

    def remove_on(self, block):
        pass                                                                                            #TODO implement ##############################################################

    def set_on(self, block_a, block_b):
        """
        Establishes relation on(block_a, block_b)
        :param block_a: block to be on top
        :param block_b: block to be on bottom
        :return: None
        """

        assert self.check_block(block_a), 'No such block: %block_a'                                     # If any argument does not correspond to an existing block, then crash
        assert self.check_block(block_b), 'No such block: %block_b'                                     # If any argument does not correspond to an existing block, then crash

        self.cursor.execute("INSERT INTO on_relation VALUES('%s', '%s')" % (block_a, block_b))
        self.db.commit()

    def check_block_type(self, block_name, type_name):
        """
        Check whether block_name is of type type_name
        :param block_name: block name
        :param type_name: type name
        :return: True if block_name is of type type_name, False otherwise
        """
        assert self.check_type(type_name), 'No such type: %s' % type_name                               # If there is no such type type_name, then crash
        assert self.check_block(block_name), 'No such block: %s' % block_name                           # If block_name doesn't exist, then crash

        self.cursor.execute("SELECT %s FROM instance WHERE name='%s'" % (type_name, block_name))
        return self.cursor.fetchone()[0] == 1

    def set_block_type(self, block_name, type_name, membership='1'):
        """
        Set type membership in 'type' to 'membership' for 'block'
        :param block: String: Name of block
        :param type: String: Name of type being set
        :param membership: Boolean: True for is member, False for is not member
        :return: None
        """
        assert self.check_type(type_name), 'No such type: %s' % type_name                               # If there is no such type type_name, then crash
        assert self.check_block(block_name), 'No such block: %s' % block_name                           # If block_name doesn't exist, then crash

        self.cursor.execute("UPDATE instance SET %s=%s where name='%s'" %
                            (type_name, ('1' if membership else '0'), block_name))
        self.db.commit()

    def display_data(self):
        """
        Prints the contents of all tables.
        :return: None
        """
        toreturn = ''

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [f[0] for f in self.cursor.fetchall()]
        for table in tables:
            toreturn += 'Table %s: ' % table
            self.cursor.execute("SELECT * FROM %s" % table)
            toreturn += str([f[0] for f in self.cursor.description]) + '\n'
            self.cursor.execute("SELECT * FROM %s" % table)
            for t in self.cursor.fetchall():
                toreturn += str(t) + '\n'
            toreturn += '\n'

        return toreturn


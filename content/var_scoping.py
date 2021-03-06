#
# this is a contrived example designed to teach variable scoping behavior.
#
# usage:
#
#     opsmop apply content/var_scoping.py
#
# ==============================================================================

from opsmop.core.easy import *

# ==============================================================================

class One(Role):

    def set_variables(self):
        return dict(glorp='fizz', level='one')

    def set_resources(self):

        return Resources(
            Debug(),
            Asserts(foosball=1, glorp='fizz', blarg=5150, other=True, level='one'),
            Set(level='runtime'),
            # SetGlobal(blippy='foo'),
            Resources(
                Set(level='nested'),
                # Asserts(level='nested'),
            ),
            Asserts(level='runtime'),
        )

# ==============================================================================

class Two(Role):

    def set_variables(self):
        return dict(level='two')

    def set_resources(self):

        res = Resources()

        res.add([
            Debug(),
            Echo("foosball={{ foosball }}")
        ])

        res.add([
            # Asserts(blippy='foo'),   
            Asserts(blarg=5150, level='two'),
            # some alternate ways to do things, more as a proof of internals
            Asserts('blarg > 3000'),
            Debug('blarg', 'foosball', random=Eval('2 * blarg + 1000'))
        ])

        return res

# ==============================================================================

class ScopeTest(Policy):

    def set_variables(self):
        return dict(level='Scope', other=True)

    def set_roles(self):
        return Roles(
            One(foosball=1),
            Two(foosball=2),
            Two(foosball=3)
        )

if __name__ == '__main__':
    Cli(ScopeTest(blarg=5150))


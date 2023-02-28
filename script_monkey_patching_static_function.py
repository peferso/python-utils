import some_package.module_1 as module_1

print('First we do not monkey patch')

instance = module_1.aClass()

print('Let us call the class method...')

instance.print_hello_world()

print('Now, let us modify the static method')

def new_function():
    return 'HELLO WORLD'

module_1.a_static_function = new_function

print('The monkey patch is done, let us call the static function')

module_1.a_static_function()

print('Now, lets create a new class instance and call the class method that calls the static one')

instance_2 = module_1.aClass()

instance_2.print_hello_world()

print('If we call the same method but with the old instance:')

instance.print_hello_world()

print('done')




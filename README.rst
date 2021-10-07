PLox
====

Plox is a Python implementation of the `Lox Programming Language
<https://www.craftinginterpreters.com/the-lox-language.html>`_, which was
created by Bob Nystrom for his book - "Crafting Interpreters".

Using Lox
---------

This is a very brief primer on how to use "Lox". For more detailed
documentation, please refer to `"Crafting Interpreters" - Chapter 3 - The Lox
Programming Language"
<http://craftinginterpreters.com/the-lox-language.html>`_.

**Input and Output**

Being a simple language created for the sake of teaching compiler design, Lox
only support one I/O operation - printing on screen.

The ``print`` statement is baked right into the core library itself. Since it's
a statement, and not a function, it should be called without the parentheses.

In fact, we are ready for our very first program::

    print "Hello, world!";

**Comments**

Anything after ``//`` is ignored as a comment.

**Data Types**

There are four basic data types:

- **Strings** - Anything quoted in double quotes is considered a string.

- **Numbers** - All numbers are stored as double precision floating point
  numbers.

- **Boolean** - It wouldn't make much sense to create a programming language
  which can't support with logic. And For logic, we need Boolean - ``true`` and
  ``false``. It follows Ruby style - only ``nil`` and ``false`` are "treated"
  as false (for eg. let's say in an if condition), everything else is
  considered true.

- ``nil`` - It represents no value. What ``None`` is to Python, what ``null``
  is to Java, ``nil`` is to Lox.

**Variables**

Lox is a dynamically typed language, and no data type is associated with
variables.

A variable can be declared using: ::

    var hello = "Hello!";

However, the initializer isn't necessary. You may choose to initialize the
variable later on. For eg.::

    var my_var;
    // More code
    my_var = "This is the best variable I named!"

**Functions**

Defining a function is fun using the keyword ``fun``: ::

    fun greet(person, host){
        print "Hello, have a good day, " + person;
        print "From,";
        print host;
    }

Calling a function: ::

    my_function("dear 'loxer'", "Rahul");

**Classes**

[Coming Soon]

Installation
------------

``plox`` can be installed using ``pip``.

Clone the repository using git: ::

    $ git clone https://github.com/RJ722/plox && cd plox

Create a virtualenv and install using ``pip``: ::

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -e .

Try it out in an interactive prompt: ::

    (venv) $ plox


Why didn't you just use the Java implementation?
------------------------------------------------

The simple answer is that I don't know Java well enough.

Also, I believe that I would learn better if rather than merely copying code, I
write it myself, and writing in another language enabled me to do just that.
Due to this, I cannot vouch for the correctness of the code. It is solely based
on my understanding of Bob's ideas.

Is this complete?
-----------------

Not yet, Classes and Inheritance (Chapter 12 and 13) are still a WIP. You
might want to watch the repo for updates.

I also (rather ambitiously) plan to complete all the Challenges listed at the
end of the chapters and publish the solutions online.

Why isn't there a LICENSE?
--------------------------

The book "Crafting Interpreters"* licenses all of it's code under the
permissible MIT License, but all the text and the aesthetics are covered under
CC BY-NC-ND 4.0. I was a little confused with this because Lox didn't fall into
neither. Also, I couldn't find a coherent licensing policy from looking at the
other ports, so I have emailed Bob (original author and creator).

Source code is open source, because there's no reason it shouldn't be, but I'd
request you all to please wait for Bob's reply in case you want to use this
code.

Similar Projects
----------------

Lox is hugely popular and the interpreter has been developed in 30+ languages.
Some of them can be found `here
<https://github.com/munificent/craftinginterpreters/wiki/Lox-implementations>`_.

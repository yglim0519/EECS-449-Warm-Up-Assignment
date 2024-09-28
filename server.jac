walker interact {
    can return_message with `root entry {
        report {
            "response": "Hello, world!"
        };
    }
}

walker interact_with_body {
    has name: str;

    can return_message with `root entry {
        report {
            "response": "Hello, " + self.name + "!"
        };
    }
}

walker add_numbers {
    has num1: int;
    has num2: int;

    can calculate with `root entry {
        result = self.num1 + self.num2;
        report {
            "result": result,
            "message": "The sum of num1 and num2 is calculated successfully!"
        };
    }
}

walker greet_user {
    has name: str;

    can say_hello with `root entry {
        greeting = "Hello, " + self.name + "! Welcome!";
        report {
            "greeting": greeting,
            "message": "User greeted successfully!"
        };
    }
}


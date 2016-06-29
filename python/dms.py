import random

class Life():
    def __init__(self, age):
        self.age = age

class Plan():
    
    def __init__(self):
        self.status = True if random.randrange(0, 2) else False

    def again(self):
        self.status = True if random.randrange(0, 2) else False

def main():
    life = Life(88)
    nowage = 22

    while  nowage <= life.age:
        print 'I have something to do!'
        plan = Plan()
        while not plan.status:
            print 'Come on!'
            plan.again()
        print 'What a beautiful day!'
        nowage += 1
    print 'No regrets.'

if __name__ == '__main__':
    main()
        
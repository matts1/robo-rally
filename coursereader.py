import os
import re
import sqlite3

os.system('rm data.sqlite3')
os.system('echo "no\n" | python manage.py syncdb')

DB = sqlite3.connect('data.sqlite3')
def query(cmd, *args):
    cursor = DB.cursor()
    cursor.execute(cmd, args)
    return cursor.fetchone()

regex = re.compile('([a-z ]+): ?([^\n]*[^:]*)\n', re.M | re.S | re.I)

def get_all_courses():
    for course in os.listdir('courses'):
        f = 'courses/' + course
        Course(f)
    DB.commit()
    DB.close()

regex = re.compile('([a-z ]+): ?([^\n]*[^:]*)\n', re.M | re.S | re.I)

class Course():
    def __init__(self, fname):
        self.fname = fname
        self.created = False
        if query('SELECT filename FROM courses_course WHERE filename=?', self.fname) is None:
            self.create_from_file(fname)

    def create_from_file(self, fname):
        data = open(fname, 'rU').read() + '\n'
        course = re.findall(regex, data)
        course = [(x[0].lower(), x[1].strip()) for x in course]
        data = dict(course)
        self.name = data['name']
        self.description = data['description']
        self.rules = data.get('rules', '').split(' ')
        self.rules_description = data.get('special rules', ' '.join(self.rules))
        self.length = data['length']
        self.difficulty = data['difficulty']
        self.min_players, self.max_players = map(int, data['players'].split())
        tags = []

        if 'flags' in data:
            for i, flag in enumerate(data['flags'].split(' ')):
                boardy, boardx, y, x = map(int, flag.split(','))
                tags.append((boardx, boardy, x, y, ':f' + str(i+1)))

        boards = {}
        if 'sboard' in data:
            index = [x[0] for x in course].index('sboard')
            assert course[index-1][0] == 'newsboard', 'invalid file'
            board = course[index-1][1].split('\n')
            for i, loc in enumerate(board[1].strip().split(' ')):
                y, x = map(int, loc.split(','))
                tags.append((0, 3, x, y, ':s' + str(i+1)))
            board = [line.split(' ') for line in board[2:-1]]
            boards[(0, 3)] = board

            course.pop(index)
            course.pop(index - 1)
        else:
            for i, loc in enumerate(data['start'].split(' ')):
                boardy, boardx, y, x = map(int, loc.split(','))
                tags.append((boardx, boardy, x, y, ':s' + str(i+1)))

        while 'newboard' in [x[0] for x in course]:
            index = [x[0] for x in course].index('newboard')
            assert course[index + 1][0] == 'board', 'invalid file'
            board = course[index][1].split('\n')[1:]
            other = course[index + 1][1].replace(',', ' ').split(' ')
            y, x, rot = map(int, other[:3])
            assert rot == 0, 'You can\'t rotate the board'
            board = [line.split(' ') for line in board[:-1]]
            boards[(x, y)] = board

            course.pop(index + 1)
            course.pop(index)

        for boardx, boardy, x, y, tag in tags:
            boards[(boardx, boardy)][y-1][x-1] += tag

        minx = min(boards, key=lambda x: x[0])[0]
        maxx = max(boards, key=lambda x: x[0])[0]
        miny = min(boards, key=lambda x: x[1])[1]
        maxy = max(boards, key=lambda x: x[1])[1]
        course = [[None] * (maxx - minx + 1) for i in range(maxy - miny + 1)]
        for (x, y), board in boards.items():
            course[y - miny][x - minx] = board

        # find correct height and width for each row
        row_height = []
        for row in course:
            heights = [-1 if board is None else len(board) for board in row]
            heights = set(heights) - set([-1])
            assert len(heights) == 1,\
                'inconsistent height in rows over multiple boards'
            row_height.append(list(heights)[0])

        col_width = []
        for i in range(len(course[0])):
            col = [course[j][i] for j in range(len(course))]
            widths = [-1 if board is None else len(board[0]) for board in col]
            widths = set(widths) - set([-1])
            assert len(widths) == 1,\
                'inconsistent width in columns over multiple boards'
            col_width.append(list(widths)[0])

        # fill in the blank boards
        for y in range(len(course)):
            for x in range(len(course[0])):
                if course[y][x] is None:
                    h = row_height[y]
                    w = col_width[x]
                    course[y][x] = [['pbbbb'] * w for i in range(h)]

        # connect the boards together
        newcourse = []
        for boardy, boardrow in enumerate(course):
            start_height = 0 if boardy == 0 else row_height[boardy-1]
            newcourse.extend([[] for i in range(row_height[boardy])])
            # make it a cumulative array
            row_height[boardy] += start_height
            for boardx, boardcol in enumerate(boardrow):
                for sqy, row in enumerate(boardcol):
                    for sq in row:
                        newcourse[start_height + sqy].append(sq)

        self.flags = {}
        self.spawn = {}
        self.board = []
        for y, row in enumerate(newcourse):
            self.board.append([])
            for x, square in enumerate(row):
                square = square.split(':')
                self.board[y].append(square[0])
                for special in square[1:]:
                    if special[0] == 's':
                        self.spawn[int(special[1:])] = (x, y)
                    elif special[0] == 'f':
                        self.flags[int(special[1:])] = (x, y)

        self.flags = [self.flags[i] for i in sorted(self.flags.keys())]
        self.spawn = [self.spawn[i] for i in sorted(self.spawn.keys())]

        convert = lambda x: ' '.join([','.join(map(str, i)) for i in x])

        print 'inserting', self.fname
        query('INSERT INTO courses_course VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            self.fname, self.name, self.description, ' '.join(self.rules),
            self.rules_description, self.length, self.difficulty,
            self.min_players, self.max_players, convert(self.spawn), convert(self.flags),
            '\n'.join([' '.join(l) for l in self.board])
        )

get_all_courses()

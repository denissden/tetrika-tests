


def appearance_old(intervals):
    lesson_start, lesson_end = intervals['lesson']
    pupil = intervals['pupil']
    tutor = intervals['tutor']

    pupil_index = 0
    tutor_index = 0

    pupil_online = False
    tutor_online = False

    both_online_secs = 0
    
    period_start = None
    while pupil_index < len(pupil) and tutor_index < len(tutor):
        p = pupil[pupil_index]
        t = tutor[tutor_index]

        if p >= t:
            tutor_index += 1
            tutor_online = not tutor_online
            curr_time = t
        else:
            pupil_index += 1
            pupil_online = not pupil_online
            curr_time = p

        if tutor_online and pupil_online and lesson_start < curr_time < lesson_end:
            period_start = curr_time
        elif period_start is not None:
            if period_start < lesson_start:
                period_start = lesson_start
            if curr_time > lesson_end:
                curr_time = lesson_end
            both_online_secs += curr_time - period_start

        print(f'{"+" if lesson_start < curr_time < lesson_end else "-"} {curr_time} {f"t {int(tutor_online)}" if p >= t else f"p {int(pupil_online)}"}: {both_online_secs}')
    print(f"end {both_online_secs}\n\n")
    return both_online_secs

def intersect(first: list, second: list):
    first_index = 0
    second_index = 0

    first_toggle = False
    second_toggle = False

    intersection = []
    both_intersect = False

    while first_index < len(first) and second_index < len(second):
        f = first[first_index]
        s = second[second_index]

        if s >= f:
            first_index += 1
            first_toggle = not first_toggle
            current = f
        else:
            second_index += 1
            second_toggle = not second_toggle
            current = s

        if first_toggle and second_toggle:
            intersection.append(current)
            both_intersect = True
        elif both_intersect:
            intersection.append(current)
            both_intersect = False
    
    return intersection
        
def count_time(periods: list):
    time = 0
    for i in range(1, len(periods), 2):
        time += periods[i] - periods[i - 1]
    return time

def appearance(intervals):
    pupil = intervals['pupil']
    tutor = intervals['tutor']
    lesson = intervals['lesson']

    pupil_and_tutor = intersect(pupil, tutor)
    account_lesson = intersect(lesson, pupil_and_tutor)

    return count_time(account_lesson)


tests = [
    {'data': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395,
1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443,
1594666473]},
     'answer': 3117
    },
    {'data': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
 
    'tutor': [1594692017, 1594692066, 1594692068,
    1594696341]},
        'answer': 3565
    }, 
    # тест ниже программа не проходит потому, что в pupil список таймстемпов не отсортирован
    # не может же быть, что ученик вышел с урока и зашел в прошедшем времени 🤨
    {'data': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542,
1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582,
1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480,
1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875,
1594706502, 1594706503, 1594706524, 1594706524, 1594706579,
1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148,
1594705149, 1594706463]},
    'answer': 3577
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['data'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
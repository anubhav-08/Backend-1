from codechef.scraper import contestScraper, problemScraper, profilePageScraper


def OffsetLoader(contest_type):

    requested_contests = []
    for i in range(0, 60, 20):
        #offset {0, 20, 40} for multiple pages of contests.
        contests_data = contestScraper(i, contest_type)

        for contests in contests_data['contests']:
            requested_contests.append(contests)

    return requested_contests


def getContestDivision(contest_id):

    contest_req = problemScraper(contest_id)
    subcontests = []
    if contest_req['is_a_parent_contest'] != True:
        subcontests.append(contest_id)
    else:
        for div in contest_req['child_contests']:
            if div == "all":
                continue
            contest_code = contest_req['child_contests'][div]['contest_code']
            subcontests.append(contest_code)

    return subcontests


def ContestData(type):

    contests_data = OffsetLoader(type)
    all_contests = []
    dateDict = {
        "Jan": "January",
        "Feb": "February",
        "Mar": "March",
        "Apr": "April",
        "May": "May",
        "Jun": "June",
        "Jul": "July",
        "Aug": "August",
        "Sep": "September",
        "Oct": "October",
        "Nov": "November",
        "Dec": "December"
    }
    for contest in contests_data:
        childContests = getContestDivision(contest['contest_code'])

        for contest_id in childContests:
            contest_temp_date = contest['contest_start_date']
            contest_updated_date = contest_temp_date[:3] + dateDict[
                contest_temp_date[3:6]] + contest_temp_date[6:]
            finalContestData = {
                "Name": contest['contest_name'],
                "ContestCode": contest_id,
                "Duration": contest['contest_duration'],
                "StartTime": contest_updated_date,
                'ContestURL': "https://www.codechef.com/" + contest_id
            }

            all_contests.append(finalContestData)

    return all_contests


def ProblemData(contest_code):
    problem_url_temp = f"https://www.codechef.com/{contest_code}/problems/"
    platform = 'C'

    problem_data = problemScraper(contest_code)
    all_problems = []

    for prob_code in problem_data["problems"]:
        finalProblemData = {
            "Name": problem_data["problems"][prob_code]["name"],
            "ProblemCode": prob_code,
            "ProblemURL": problem_url_temp + prob_code,
            "ContestId": contest_code,
            "Platform": platform
        }
        all_problems.append(finalProblemData)

    return (all_problems)


def contestgivenScrapper(user_handle):

    soup = profilePageScraper(user_handle)

    contests = soup.find('article')
    contests = contests.find_all('p')

    contests_given = []
    for contest in contests:
        cont = contest.find('strong').contents
        contests_given.append(cont[0][:-1])

    if contests_given[0] == "Practice":
        contests_given = contests_given[1:]

    return contests_given


def problems_solved(user_handle):

    soup = profilePageScraper(user_handle)
    print(user_handle)
    upsolved_problems = []
    problems_solved_in_contests = []

    all_contests = soup.find('article')
    contests_list = all_contests.find_all('p')
    cont = (contests_list[0].find('strong').contents)[0][:-1]

    if cont == "Practice":
        probs = contests_list[0].find_all('a')
        for prob in probs:
            upsolved_problems.append(prob.contents[0])

    probs = all_contests.find_all('a')

    for prob in probs:
        temp = prob.contents[0]
        if not temp in upsolved_problems:
            problems_solved_in_contests.append(temp)

    return (upsolved_problems, problems_solved_in_contests)


def userScraper(user_handle):

    soup = profilePageScraper(user_handle)
    user_details = soup.find('section', class_='user-details')

    name = soup.find('div', class_='user-details-container plr10')
    name = name.find('h1').contents[0]

    country = user_details.find('span', class_='user-country-name').contents[0]

    rating = soup.find('div', class_='rating-header')

    user_rating = soup.find('div', class_='rating-number')
    user_rating = (user_rating.contents)[0]

    user_stars = rating.find('div', class_='rating-star')
    user_stars = len(list(user_stars.find_all('span')))

    user_highest_rating = (rating.find('small').contents)[0]
    user_highest_rating = str(user_highest_rating).split(' ')[-1][:-1]

    ranks = soup.find('div', class_='rating-ranks')
    ranks = ranks.find_all('strong')
    global_rank = ranks[0].contents[0]
    country_rank = ranks[1].contents[0]

    # user, isCreated = User.objects.get_or_create(handle=user_handle, username=user_handle)
    # user.name = name
    # user.stars = user_stars
    # user.rating = int(user_rating)
    # user.maxRating = int(user_highest_rating)
    # user.country = country
    # user.country_rank = country_rank
    # user.global_rank = global_rank
    # user.save()

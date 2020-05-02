import urllib.request
import urllib.parse
from datetime import date, datetime
import os

from googleapiclient.discovery import build


def google_query(query, api_key, cse_id, **kwargs):
    query_service = build("customsearch",
                          "v1",
                          developerKey=api_key
                          )

    query_results = query_service.cse().list(q=query,  # Query
                                             cx=cse_id,  # CSE ID
                                             **kwargs
                                             ).execute()
    return query_results['items']


def runScript(options):
    api_key = "AIzaSyC82PPB7gNUXaoyZrf9000NTYFzoomSjC0"
    cse_id = "007736650077175064536:jukxmfl0vgf"

    my_results_set = set()
    today = date.today().strftime("%Y%m%d")
    animal = options.animal
    dateFrom = options.dateFrom
    dateTo = options.dateTo
    terms = options.terms
    numOfSearchResults = options.numOfSearchResults
    numOfResultsPerPage = 10
    sno = options.sno
    downloadPath = f"Q{sno}_{animal}_from({dateFrom})_to({dateTo})_on({today})"
    for i in range(int(numOfSearchResults / numOfResultsPerPage)):
        for v in terms.split("|"):
            q = v + " " + animal
            my_results = google_query(q,
                                      api_key,
                                      cse_id,
                                      start=i * numOfResultsPerPage + 1,
                                      num=numOfResultsPerPage,
                                      sort=f"date:r:{dateFrom}:{dateTo}",
                                      orTerms=f"{terms}|{animal}"
                                      )
            for result in my_results:
                iri = result['link']
                split_url = list(urllib.parse.urlsplit(iri))
                split_url[2] = urllib.parse.quote(split_url[2])  # the third component is the path of the URL/IRI
                url = urllib.parse.urlunsplit(split_url)
                my_results_set.add((url,
                                    result['title']))

    for link, title in my_results_set:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '
                              'Safari/537.3'}
            req = urllib.request.Request(url=link, headers=headers)
            response = urllib.request.urlopen(req)
            webContent = response.read()
            os.makedirs(downloadPath, exist_ok=True)
            f = open(f"{downloadPath}/{title}" + ".html", 'wb')
            f.write(webContent)
            f.close()
            print(f"Saved - {link} - {title}")
        except:
            print(f"NotSaved - {link} - {title}")

    print("****-------------------------------------------------------------***")
    print(f"Run for query num {sno} with path {downloadPath} completed on : ",
          datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("****-------------------------------------------------------------***")


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-a", "--animal", type="string", help="animal", dest="animal", default="pangolin")
    parser.add_option("-f", "--dateFrom", type="string", help="date from", dest="dateFrom", default="20100101")
    parser.add_option("-t", "--dateTo", type="string", help="date to", dest="dateTo", default="20201231")
    parser.add_option("-s", "--searchTerms", type="string", help="search terms", dest="terms",
                      default="seize|seizure|poach")
    parser.add_option("-n", "--numresults", type="int", help="number of search results", dest="numOfSearchResults",
                      default=10)
    parser.add_option("-m", "--serialno", type="int", help="serial no of query", dest="sno",
                      default=0)

    options, arguments = parser.parse_args()

    runScript(options)

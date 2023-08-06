import os
import requests
import json

class UserAction():
    MIN=0
    UNRESOLVED=0
    YES=1
    NO=2
    RESOLVED=3
    MAX=3

class Client:

    def __init__(self):
        if 'RAYYAN_STORE_URL' not in os.environ:
            raise RuntimeError('RAYYAN_STORE_URL environment variable not found')
        self.url = os.environ['RAYYAN_STORE_URL']
        self.session = requests.Session()

    def create_review(self, review_id):
        return self.__post_request("/reviews/{}".format(review_id))

    def delete_review(self, review_id):
        return self.__delete_request("/reviews/{}".format(review_id))

    def import_articles(self, review_id, articles):
        return self.__post_request("/import", {
            'review_id': review_id,
            'articles': map(lambda a: filter(lambda k,v: v and v != '', a), articles)
        })["article_ids"]

    def delete_by_file_id(self, review_id, file_id):
        return self.__delete_request("/delete-by-file-id/{}".format(file_id), {
            review_id: review_id
        })

    def export(self,review_id, source, last_id, length):
        """
        Exports specified articles from rayyan-store.
        Use stream_export for better performance.

        Returns:
            tuple: (array of exported articles in JSON, last_id)

        """
        attribute = 'id' if source == 'articles' else 0

        results = self.__get_request('export', {
            "review_id": review_id,
            "source": source,
            "last_id": last_id,
            "length": length
        })

        if len(results) > 0:
            last_id = results[-1][attribute]

        return (results, last_id)

    def stream_export(self, review_id, source):
        """
        Streaming version of export.

        Returns:
            generator to each exported JSON object.
        """

        response = self.__chunked_get_request('/stream-export', {
            'review_id': review_id,
            'source': source
        })

        for line in response.iter_lines():
            yield json.loads(line.decode('utf-8'))

    def query(self, review_id, filter = {}, start_index = 0, length = 30,
            return_total = False, sort_key = 'id', sort_dir = 'asc'):
        """
        Returns:
            tuple: (array of articles in JSON, total)

        """
        response = self.__get_request('/query', {
            'review_id': review_id,
            'start_index': start_index,
            'length': length,
            'return_total': 1 if return_total else 0,
            'sort_key': sort_key,
            'sort_dir': sort_dir
        }, {
            'filter': filter
        })

        articles = response["articles"]

        if return_total:
            return (articles, response["total"])
        else:
            return (articles, None)

    def total(self, review_id):
        return self.__get_request('/total', {
            "review_id": review_id
        })["total"]

    def facet(self, review_id, key, user_ids, limit=10):
        return self.__get_request("/facet/{}".format(key), {
            "review_id": review_id,
            "user_ids": user_ids.join(',') if user_ids else None,
            "limit": limit
        })

    def insert_customization(self, review_id, article_id, user_id, key, value = 1):
        return self.__post_request('/customization', {
            "review_id": review_id,
            "article_id": article_id,
            "user_id": user_id,
            "key": key,
            "value": value
        })

    def delete_customization(self, review_id, article_id, user_id, key):
        return self.__delete_request('/customization', {
            "review_id": review_id,
            "article_id": article_id,
            "user_id": user_id,
            "key": key
        })

    def insert_dedup_results(self, review_id, dedup_results, nullify = True):
        '''
        Inserts multiple dedup results into respective articles.
        Objects in 'dedup_results' must have the form:
            {
                "article_id": ... (int),
                "dedup_job_id": ... (int),
                "cluster_id": ... (int),
                "score": ... (str),
                "user_action": ... (UserAction),
            }
        If 'nullify' is true, all previous, non-deleted dedup_results
        will be erased.
        '''
        # TODO: Validate 'documents' to ensure fields.

        return self.__post_request('/insert-dedup',
                {
                    "review_id": review_id,
                    "dedup_results": dedup_results,
                    "nullify": nullify
                })

    def update_dedup_user_action(self, review_id, article_id, user_action):
        '''
        Updates the user action of a single article.

        NOTE: 'user_action' must be a UserAction constant.
        '''
        # TODO: Validate 'document' to ensure 'article_id' and 'user_action' fields.

        return self.__post_request('/update-dedup',
                {
                    "review_id": review_id,
                    "article_id": article_id,
                    "user_action": user_action
                })

    ## Private methods

    def __request(self, method, path, query = None, body = None, isStreaming=False):
        """
        Underlying function for all requests.

        Args:
            method: HTTP method to use
            path: routing path for the app
            query: JSON object encoding a query string.
            body:  JSON object encoding request body.
            isStreaming: Enable/disable HTTP streaming.

        Returns:
            if isStreaming:
                requests.response object
            else:
                JSON object encoding the response.
                (Should be an array of articles)
        """
        review_id = None
        if query and "review_id" in query:
          review_id = query["review_id"]
        elif body and "review_id" in body:
          review_id = body["review_id"]
        else:
          review_id = path.split('/')[1]

        method = method.upper()
        response = self.session.request(method, path,
                            params=query,
                            stream=isStreaming,
                            json=body,
                            headers={ "X-Review-ID": str(review_id) })

        if response.status_code != 200:
            err = (method, path, response.status_code, response.text)
            raise RuntimeError("Error in {} {} [{}]: {}".format(*err))

        if isStreaming:
            return response
        else:
            return response.json()

    def __chunked_get_request(self, path, query, body=None):
        return self.__request("GET", self.url+path, query, body, isStreaming=True)

    def __get_request(self, path, query, body=None):
        return self.__request("GET", self.url+path, query, body)

    def __post_request(self, path, body=None):
        return self.__request("POST", self.url+path, None, body)

    def __delete_request(self, path, body=None):
        return self.__request("DELETE", self.url+path, None, body)






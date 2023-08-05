from cnd_io.cnd_provider import CndProvider
import requests
import json


class CndProviderGitlab(CndProvider):
    def __init__(self, creds={}, print=None):
        super().__init__(creds=creds, print=print)
        self._private_token = creds["private_token"]
        self._host = creds["host"]
        self._source_name = None
        self.default_headers = {
            "Content-Type": "application/json", 
            "PRIVATE-TOKEN": self._private_token
        }

    def _query(self, url, method="get", json_data={}):
        if method not in ['get', 'post', 'delete', 'patch', 'put']:
            raise AttributeError("(CND) Method not allowed")
        full_url = f"{self._host}{url}"
        if method == 'get':
            response = requests.get(full_url, headers=self.default_headers, verify=True)

        if method in ['post', 'delete', 'patch', 'put']:
            self._print.trace_d(f"Json Data: {json_data}")
            response = getattr(requests, method)(full_url, headers=self.default_headers, json=json_data, verify=True)
        self._print.trace_d(f"Full url: {full_url}")
        self._print.trace_d(f"Method: {method}")
        self._print.trace_d(f"Status Code: {response.status_code}")
        self._print.trace_d(f"Content: {response.content}")
        if response.status_code in [200, 201, 202, 404]:
            return response
        return False

    def _get_blob(self, blob_id):
        url = f"projects/{self._source_name}/repository/blobs/{blob_id}/raw"
        response = self._query(url)  
        if response is False:
            return False
        return response.content.decode() 

    def _get_blob_id(self, file_path, branch):
        url = f"projects/{self._source_name}/repository/files/{file_path}?ref={branch}"
        response = self._query(url)
        if response is False:
            return False
        if response.status_code == 404:
            return None
        json_content = json.loads(response.content)
        return json_content['blob_id']

    def pull_file(self, source_name, file_path, branch="main"):
        self._source_name = source_name
        blob_id = self._get_blob_id(file_path=file_path, branch=branch)
        raw_content = self._get_blob(blob_id)
        return raw_content

    def push_file(self, source_name, file_name, content, commit_message="It's a so nice day today", branch="main"):
        return self.push_files(source_name, [{'file_path': file_name, 'content': content}], commit_message=commit_message, branch=branch)

    def push_files(self, source_name, files, commit_message="It's a so nice day today", branch="main"):
        self._source_name = source_name
        url = f"projects/{self._source_name}/repository/commits"
        payload = {
            "branch": branch,
            "commit_message": commit_message,
            "actions": []
        }
        for file in files:
            data = {
                        "file_path": file,
                        "content": files[file]
                    }
            blob_id = self.file_exist(source_name, file, branch)
            if blob_id is  None:
                data["action"] = 'create'
            else:
                content = self._get_blob(blob_id)
                if content == files[file]:
                    self._print.trace_e(f'Identical file, skipping {file}')
                    continue
                data["action"] = 'update'
            payload["actions"].append(
                data
            )
        if len(payload["actions"]) == 0:
            return None
        result = self._query(url, method='post', json_data=payload)
        return result.status_code == 201

    def file_exist(self, source_name, file_path, branch="main"):
        self._source_name = source_name
        blob_id = self._get_blob_id(file_path, branch)
        return blob_id

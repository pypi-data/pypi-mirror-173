"""

    """

import shutil
from pathlib import Path

from dulwich import index
from dulwich import porcelain
from dulwich.client import HTTPUnauthorized

from .consts import Consts
from .funcs import clean_github_url
from .funcs import get_github_tok_fp
from .funcs import get_github_usr_tok_fr_js_file
from .funcs import github_url_wt_credentials


cte = Consts()


class Repo :

    def __init__(self , src_url , github_usr = None , usr_tok_json_fp = None) :
        self.src_url = src_url
        self.github_usr = github_usr
        self.usr_tok_json_fp = usr_tok_json_fp

        self.cln_src_url = clean_github_url(src_url)
        self.user_repo = self.cln_src_url.split(cte.gi)[1]
        self.user_name = self.user_repo.split('/')[0]
        self.repo_name = self.user_repo.split('/')[1]

        self._init_local_path()

    @property
    def local_path(self) :
        return self._local_path

    @local_path.setter
    def local_path(self , local_dir) :
        if local_dir is None :
            self._local_path = Path(self.repo_name)
        else :
            self._local_path = Path(local_dir)

        if self._local_path.exists() :
            print(f'WARNING: {self._local_path} already exists')

    def _init_local_path(self) :
        self.local_path = None

    def _stage_all_changes(self) :
        idx = self._repo.open_index()

        lp = str(self.local_path) + '/'
        fu = porcelain.get_untracked_paths
        untracked = fu(lp , lp , idx , exclude_ignored = True)

        unstaged = index.get_unstaged_changes(idx , self.local_path)

        all_changes = list(unstaged) + list(untracked)

        self._repo.stage(all_changes)
        return all_changes

    def _input_cred_usr_tok(self) :
        if not self.github_usr :
            msg = '(enter nothing for same as repo source) github username: '
            self.github_usr = input(msg)
            if self.github_usr.strip() == '' :
                self._crd_usr = self.user_name
        else :
            self._crd_usr = self.github_usr

        tok = input('token: ')
        self._crd_tok = tok

    def _set_cred_usr_tok_fr_file(self , fp , github_usr = None) :
        o = get_github_usr_tok_fr_js_file(fp , usr = github_usr)
        self._crd_usr , self._crd_tok = o.usr , o.tok

    def _set_cred_usr_tok(self) :
        fp = self.usr_tok_json_fp
        if fp :
            self._set_cred_usr_tok_fr_file(fp , github_usr = self.github_usr)
            return

        fp = Path('tok.json')
        if fp.exists() :
            self._set_cred_usr_tok_fr_file(fp)
            return

        fp = get_github_tok_fp()
        if fp :
            self._set_cred_usr_tok_fr_file(fp , github_usr = self.github_usr)
            return

        self._input_cred_usr_tok()

    def _set_clone_url(self) :
        self._set_cred_usr_tok()
        usr = self._crd_usr
        tok = self._crd_tok
        tr = self.user_repo
        self._clone_url = github_url_wt_credentials(usr , tok , tr)

    def overwriting_clone(self , overwrite = True , depth = 1) :
        """ Every time excecuted, it re-downloads last version of the reposiroty to local_path.

        param depth: None for full depth, default = 1 (last version)
        return: None
        """
        trgdir = self.local_path
        if trgdir.exists() and overwrite :
            self.rmdir()

        try :
            self._clone_url = self.cln_src_url
            url = self._clone_url
            self._repo = porcelain.clone(url , trgdir , depth = depth)

        except HTTPUnauthorized :
            self._set_clone_url()
            url = self._clone_url
            self._repo = porcelain.clone(url , trgdir , depth = depth)

    def _set_commit_url(self) :
        if not hasattr(self , '_clone_url') :
            self._clone_url = None

        if not self._clone_url == self.cln_src_url :
            self._commit_url = self._clone_url
        else :
            self._set_cred_usr_tok()
            usr = self._crd_usr
            tok = self._crd_tok
            tr = self.user_repo
            self._commit_url = github_url_wt_credentials(usr , tok , tr)

    def commit_and_push(self , message , branch = 'main') :
        self._set_commit_url()
        self._stage_all_changes()
        self._repo.do_commit(message.encode())
        porcelain.push(str(self._local_path) , self._commit_url , branch)
        print(message)

    def rmdir(self) :
        shutil.rmtree(self._local_path)

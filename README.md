# Keystone プロジェクト管理者用ポリシー調査

このレポジトリはプロジェクト管理者用の `policy.json` が Keystone に設定されていることをチェックするための、
機能テストプロジェクトを含んでいます。

## 前提

このテストプログラムを実行する際の前提条件。

-   Python 3.5 がインストールされていること。
-   tox がインストールされていること。
-   python-openstackclient がインストールされていること。
-   Keystone にクラウド管理者として `admin` ロールが作成されていること。
-   Keystone に `project_admin` ロールが作成されていること。
-   Keystone に `Member` ロールが作成されていること。
-   [policy.project-admin.json](policy.project-admin.json) が Keystone に `policy.json` として設定されていること。

## 環境変数の設定

テスト対象の OpenStack のクラウド管理者用環境変数が設定されていること。
以下は設定されていることを期待する環境変数例。

```bash
export OS_AUTH_URL=http://172.18.11.197/identity
export OS_IDENTITY_API_VERSION=3
export OS_NO_CACHE=1
export OS_PASSWORD=openstack
export OS_PROJECT_DOMAIN_ID=default
export OS_PROJECT_NAME=admin
export OS_REGION_NAME=RegionOne
export OS_USERNAME=admin
export OS_USER_DOMAIN_ID=default
```

## テストの実行

```bash
$ tox -epy35
```

### 一部のテストのみ実行

例えばユーザ作成のテストのみを実行した場合は以下のコマンドを実行する。

```bash
$ tox -epy35 -- TestUserCreate
```

### 並列実行数の変更

このテストは実際の OpenStack に API を発行するため、その数を制限するためには、
並列実行数を制限する必要があります。

```bash
# 3並列実行時の例
$ tox -epy35 -- --concurrency 3
```

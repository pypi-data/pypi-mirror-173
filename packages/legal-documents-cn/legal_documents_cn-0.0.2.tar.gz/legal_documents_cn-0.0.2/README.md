# Legal Documents CN 中文法律查询数据
```shell
pip install pandas
pip install nltk
pip install legal_documents_cn
```


```python
from legal_documents_cn import criminal_law_cn as law
law.getInfoByArticleCode(article_code=219,article_sub_code=1)
#第二百一十九条之一

```

```python
from legal_documents_cn import criminal_law_cn as law
law.getInfoByContent(content='小明交通肇事',vague=True)
#content为需要查询的条款内容，vague为模糊查询

```
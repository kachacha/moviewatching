# 部署到OpenShift

## 创建

```bash
oc new-app \
    git@gitlab.zylliondata.local:idsg/translate-tool.git \
    --allow-missing-images=true \
    --name=translate-tool
    
```

## 删除

```bash
oc delete all -l app=translate-tool

```
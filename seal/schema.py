from system.models import Users
from graphene_django import DjangoObjectType
import graphene


# 相关文档 https://passwo.gitbook.io/graphql/index/drf
class UserType(DjangoObjectType):
    class Meta:
        model = Users


class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    # List == Field:
    # List 返回结果会是遍历所有查询结果
    # Field 返回结果只存在单个 (其中可添加参数, ex. pk)
    single_user = graphene.Field(UserType, pk=graphene.Int())

    # 定义函数名的格式: resolve_字段
    # **kwargs 传递参数
    # pk: 如果在字段中定义, 则方法参数中必含
    def resolve_users(self, info, **kwargs):
        return Users.objects.all()

    def resolve_single_user(self, info, pk):
        return Users.objects.get(id=pk)


class TQuery(Query, graphene.ObjectType):
    pass


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    info = graphene.Field(UserType)
    ok = graphene.Boolean()

    def mutate(self, info, **kwargs):
        # print(info.context.user, '==当前用户==')
        # kwargs 是传递参数中的变量
        # user = info.context.user
        user_obj = Users(**kwargs)
        try:
            user_obj.save()
            ok = True
        except Exception as e:
            print(e)
            ok = False
        return CreateUser(ok=ok, info=user_obj)


class CMutation(object):
    create_user = CreateUser.Field()


class UpdateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        pk = graphene.Int(required=True)

    info = graphene.Field(UserType)
    ok = graphene.Boolean()

    def mutate(self, info, **kwargs):
        pk = kwargs.get('pk')
        user_obj = Users.objects.get(id=pk)
        if not user_obj:
            return UpdateUser(ok=False)
        user_obj.__dict__.update(**kwargs)
        user_obj.save()
        ok = True
        return UpdateUser(ok=ok, info=user_obj)


class UMutation(object):
    update_user = UpdateUser.Field()


class DeleteUser(graphene.Mutation):
    class Arguments:
        pk = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, info, **kwargs):
        pk = kwargs.get('pk')

        user = Users.objects.get(id=pk)
        user.delete()
        return DeleteUser(ok=True)


class DMutation(object):
    delete_user = DeleteUser.Field()


class Mutations(CMutation, UMutation,DMutation,graphene.ObjectType):
    pass


schema = graphene.Schema(query=TQuery, mutation=Mutations)


import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import Department as DepartmentModel
from models import Employee as EmployeeModel
from models import Role as RoleModel


class Department(SQLAlchemyObjectType):

    class Meta:
        model = DepartmentModel
        only_fields = ('name', )
        interfaces = (relay.Node, )

class Role(SQLAlchemyObjectType):

    class Meta:
        model = RoleModel
        interfaces = (relay.Node, )


class Employee(SQLAlchemyObjectType):

    class Meta:
        model = EmployeeModel
        only_fields = ('name', 'department', )  # careful limitations review required
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    allEmployees = SQLAlchemyConnectionField(Employee)
    allRoles = SQLAlchemyConnectionField(Role)
    role = graphene.Field(Role)
    node = relay.Node.Field()


schema = graphene.Schema(query=Query, types=[Department, Employee, Role])

from email.headerregistry import Address
from sqlalchemy import BigInteger, ForeignKey, PrimaryKeyConstraint, create_engine, text, Connection, MetaData, Table, String, Integer, select  # type: ignore
from sqlalchemy.orm import Mapped, Session, as_declarative, declarative_base, declared_attr, foreign, registry, mapped_column

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


@as_declarative()
class AbstractModel:
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class UserModel(AbstractModel):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column()
    fullname: Mapped[str] = mapped_column()

class AddressModel(AbstractModel):
    __tablename__ = 'addresses'
    email = mapped_column(String, nullable=False)
    user_id = mapped_column(ForeignKey('users.id'))


with Session(engine) as session:
    with session.begin():
        AbstractModel.metadata.create_all(engine)
        user = UserModel(user_id=1, name='Hayk', fullname='Hayk Manukyan')
        session.add(user)
    with session.begin():
        res = session.execute(select(UserModel).where(UserModel.user_id==1))
        user = res.scalar()
        print(user.name)
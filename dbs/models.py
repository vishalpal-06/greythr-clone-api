from sqlalchemy import (
    create_engine, Column, Integer, String, Date, DateTime, Numeric,
    Enum, ForeignKey, Table
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# Association tables
employee_role = Table(
    'employee_role', Base.metadata,
    Column('employeeID', Integer, ForeignKey('employee.employeeID'), primary_key=True),
    Column('roleID', Integer, ForeignKey('role.roleID'), primary_key=True)
)

employee_policy = Table(
    'employee_policy', Base.metadata,
    Column('employeeID', Integer, ForeignKey('employee.employeeID'), primary_key=True),
    Column('policyID', Integer, ForeignKey('company_policy.policyID'), primary_key=True),
    Column('acknowledgmentDate', Date)
)

# Department
class Department(Base):
    __tablename__ = 'department'
    departmentID = Column(Integer, primary_key=True, autoincrement=True)
    departmentName = Column(String(100), nullable=False)
    description = Column(String)
    employees = relationship("Employee", back_populates="department")

# Employee
class Employee(Base):
    __tablename__ = 'employee'
    employeeID = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15))
    hireDate = Column(Date, nullable=False)
    departmentID = Column(Integer, ForeignKey('department.departmentID'))
    managerID = Column(Integer, ForeignKey('employee.employeeID'))
    password = Column(String(255), nullable=False)
    last_login = Column(DateTime)

    # Relationships
    department = relationship("Department", back_populates="employees")
    manager = relationship("Employee", remote_side=[employeeID], back_populates="subordinates")
    subordinates = relationship("Employee", back_populates="manager")

    payrolls = relationship("Payroll", back_populates="employee")
    leaves = relationship("Leave", back_populates="employee", foreign_keys="Leave.employeeID")
    managed_leaves = relationship("Leave", back_populates="manager", foreign_keys="Leave.managerID")

    expense_claims = relationship("ExpenseClaim", back_populates="employee", foreign_keys="ExpenseClaim.employeeID")
    managed_expense_claims = relationship("ExpenseClaim", back_populates="manager", foreign_keys="ExpenseClaim.managerID")

    attendance = relationship("Attendance", back_populates="employee")
    policies = relationship("CompanyPolicy", secondary=employee_policy, back_populates="employees")
    roles = relationship("Role", secondary=employee_role, back_populates="employees")

# Payroll
class Payroll(Base):
    __tablename__ = 'payroll'
    payrollID = Column(Integer, primary_key=True, autoincrement=True)
    employeeID = Column(Integer, ForeignKey('employee.employeeID'), nullable=False)
    salaryAmount = Column(Numeric(10, 2), nullable=False)
    payDate = Column(Date, nullable=False)
    taxDeduction = Column(Numeric(10, 2))
    netPay = Column(Numeric(10, 2))

    employee = relationship("Employee", back_populates="payrolls")

# Leave
class Leave(Base):
    __tablename__ = 'leave'
    leaveID = Column(Integer, primary_key=True, autoincrement=True)
    employeeID = Column(Integer, ForeignKey('employee.employeeID'), nullable=False)
    managerID = Column(Integer, ForeignKey('employee.employeeID'))
    leaveType = Column(String(50), nullable=False)
    startDate = Column(Date, nullable=False)
    endDate = Column(Date, nullable=False)
    status = Column(Enum('Pending', 'Approved', 'Rejected'), default='Pending')

    employee = relationship("Employee", foreign_keys=[employeeID], back_populates="leaves")
    manager = relationship("Employee", foreign_keys=[managerID], back_populates="managed_leaves")

# Attendance
class Attendance(Base):
    __tablename__ = 'attendance'
    attendanceID = Column(Integer, primary_key=True, autoincrement=True)
    employeeID = Column(Integer, ForeignKey('employee.employeeID'), nullable=False)
    date = Column(Date, nullable=False)
    checkInTime = Column(DateTime)
    checkOutTime = Column(DateTime)
    status = Column(Enum('Present', 'Absent', 'Late', 'Not Completed Full Day'), nullable=False)

    employee = relationship("Employee", back_populates="attendance")

# ExpenseClaim
class ExpenseClaim(Base):
    __tablename__ = 'expense_claim'
    claimID = Column(Integer, primary_key=True, autoincrement=True)
    employeeID = Column(Integer, ForeignKey('employee.employeeID'), nullable=False)
    managerID = Column(Integer, ForeignKey('employee.employeeID'))
    claimDate = Column(Date, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(String)
    status = Column(Enum('Pending', 'Approved', 'Rejected'), default='Pending')

    employee = relationship("Employee", foreign_keys=[employeeID], back_populates="expense_claims")
    manager = relationship("Employee", foreign_keys=[managerID], back_populates="managed_expense_claims")

# CompanyPolicy
class CompanyPolicy(Base):
    __tablename__ = 'company_policy'
    policyID = Column(Integer, primary_key=True, autoincrement=True)
    policyName = Column(String(100), nullable=False)
    description = Column(String)
    effectiveDate = Column(Date, nullable=False)

    employees = relationship("Employee", secondary=employee_policy, back_populates="policies")

# Role
class Role(Base):
    __tablename__ = 'role'
    roleID = Column(Integer, primary_key=True, autoincrement=True)
    roleName = Column(String(50), unique=True, nullable=False)
    description = Column(String)

    employees = relationship("Employee", secondary=employee_role, back_populates="roles")

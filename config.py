__author__ = 'woody'
from flask import Flask
import getpass
import os
import sys,socket
import platform
app = Flask(__name__)
#公用配置,个人配置可以在父类基础上丰富
class Base:
    pass


    #所有case列表
    ALL_CASE = ['Case001','Case002','Case003','Case004','Case005','Case006','Case007','Case008','Case009','Case010',
                 'Case011','Case013','Case014','Case015','Case016','Case018','Case019',
                 'Case023','Case024','Case026','Case028','Case029',
                 'Case030','Case031','Case032','Case034','Case036','Case040','Case042','Case046','Case047','Case048', 'Case050','Case054','Case055','Case056','Case057',
                 'Case058','Case059','Case060','Case063','Case064','Case065','Case066','Case067','Case068','Case069',
                 'Case070','Case071','Case072','Case073','Case074','Case075','Case076','Case077','Case078','Case079','Case081','Case082','Case084',
                 'Case086','Case087','Case089','Case094','Case095','Case096','Case097','Case099','Case100','Case101','Case102',
                 'Case103','Case104','Case105','Case106','Case107','Case109','Case110',#'Case111','Case098','Case021',
                ]
                #,'Case108','Case045','Case037','Case039','Case017',#'Case025','Case027','Case033','Case043','Case044','Case051','Case049','Case052','Case053','Case085','Case061',,'Case062','Case012','Case020',
    # ALL_CASE = ['Case069']
    IMPORT_CASE_LIST = [
                         ('UICase.Case001huarunDiagnosis','Case001'),
                         ('UICase.Case002szhuaweiSystemListenPage', 'Case002'),
                         ('UICase.Case003simscSysListenPage', 'Case003'),
                         ('UICase.Case004userLoginAndOut', 'Case004'),
                         ('UICase.Case005huaweiIcon', 'Case005'),
                         ('UICase.Case006loginUseTime', 'Case006'),
                         ('UICase.Case007mapRedPoint', 'Case007'),
                         ('UICase.Case008addPointToDataSource', 'Case008'),
                         ('UICase.Case009dataAnalysisPages', 'Case009'),
                         ('UICase.Case010dataAnalysisWorkSpace', 'Case010'),
                         ('UICase.Case011dataAnalysisTemplate', 'Case011'),
                         ('UICase.Case012dataSouceGroup', 'Case012'),
                         ('UICase.Case013userInfo', 'Case013'),
                         ('UICase.Case014dataSourceNotes', 'Case014'),
                         ('UICase.Case015dataAnalysisPic', 'Case015'),
                         ('UICase.Case016userPasswordError', 'Case016'),
                         ('UICase.Case017wiki', 'Case017'),
                         ('UICase.Case018navigateMode', 'Case018'),
                         ('UICase.Case019smiscDashboardJump', 'Case019'),
                         ('UICase.Case020dataSourceScroll', 'Case020'),
                         ('UICase.Case021InvitePeople', 'Case021'),
                         ('UICase.Case022dataSourceSearch', 'Case022'),
                         ('UICase.Case023dashboardPointAddToDS', 'Case023'),
                         ('UICase.Case024reportCheck', 'Case024'),
                         ('UICase.Case025taskGroup', 'Case025'),
                         ('UICase.Case026dashboardData', 'Case026'),
                         ('UICase.Case027workFlowEdit', 'Case027'),
                         ('UICase.Case028itemSearch', 'Case028'),
                         ('UICase.Case029huaweiDiagnosisPage', 'Case029'),
                         ('UICase.Case030indexPageCheck', 'Case030'),
                         ('UICase.Case031huaweiDataPointLost', 'Case031'),
                         ('UICase.Case032diagnosisCreateWorkFlow', 'Case032'),
                         ('UICase.Case033workFlowTag', 'Case033'),
                         ('UICase.Case034factoryCreateItem', 'Case034'),
                         ('UICase.Case036functionRecord', 'Case036'),
                         ('UICase.Case037patrolPoint', 'Case037'),
                         ('UICase.Case039patrolPeople', 'Case039'),
                         ('UICase.Case040forgetPassword', 'Case040'),
                         ('UICase.Case041factoryEditPage', 'Case041'),
                         ('UICase.Case042factoryPageDelete', 'Case042'),
                         ('UICase.Case043messageCenter', 'Case043'),
                         ('UICase.Case044diagnosisCostTime', 'Case044'),
                         ('UICase.Case045cloudPointOutput', 'Case045'),
                         ('UICase.Case046leftAndRightDisagnosisCount', 'Case046'),
                         ('UICase.Case047shareReportLink', 'Case047'),
                         ('UICase.Case048checkHWDashboard', 'Case048'),
                         ('UICase.Case049appPageJump', 'Case049'),
                         ('UICase.Case050clickMoreButton', 'Case050'),
                         ('UICase.Case051reportCheck', 'Case051'),
                         ('UICase.Case052reportCheck', 'Case052'),
                         ('UICase.Case053reportCheck', 'Case053'),
                         ('UICase.Case054fullScreen', 'Case054'),
                         ('UICase.Case055searchPoints', 'Case055'),
                         ('UICase.Case056originalData','Case056'),
                         ('UICase.Case057livePoint','Case057'),
                         ('UICase.Case058shLFSPage','Case058'),
						 ('UICase.Case059cnLFSPage','Case059'),
						 ('UICase.Case060BugisPage','Case060'),
						 ('UICase.Case061patrolLog','Case061'),
                         ('UICase.Case062liverpoolIndexPage','Case062'),
                         ('UICase.Case063liverpoolstEnergyOverviewPage','Case063'),
                         ('UICase.Case064liverpoolstDiagnosisOverviewPage','Case064'),
                         ('UICase.Case065liverpoolstKPIOverviewPage','Case065'),
                         ('UICase.Case066liverpoolstDiagnosisPage','Case066'),
                         ('UICase.Case067liverpoolstPlantPage','Case067'),
						 ('UICase.Case068demo09IndexPage','Case068'),
						 ('UICase.Case069demo09KPISummary','Case069'),
						 ('UICase.Case070demo09EnergyCostOverview','Case070'),
						 ('UICase.Case071demo09IceStorageSystemOverview','Case071'),
						 ('UICase.Case072demo09Equipments','Case072'),
						 ('UICase.Case073demo09SystemDiagnosis','Case073'),
						 ('UICase.Case074demo09DiagnosisOverview','Case074'),
                         ('UICase.Case075jinzhongIndexpage','Case075'),
                         ('UICase.Case076checkHWIndex','Case076'),
                         ('UICase.Case077factoryProjectType','Case077'),
                         ('UICase.Case078WorkflowCheck','Case078'),
                         ('UICase.Case079WorkflowProjectCheck','Case079'),
                         ('UICase.Case081beopProjectType','Case081'),
                         ('UICase.Case082checkdisagnosisfolder','Case082'),
                         ('UICase.Case084checkdisagnosisNewPage','Case084'),
                         ('UICase.Case085importData','Case085'),
                         ('UICase.Case086MercedesEnergyOverview','Case086'),
                         ('UICase.Case087ShsmhjamQueryEnergyVal','Case087'),
                         ('UICase.Case088huaweiDiagnosisOverviewPage','Case088'),
                         ('UICase.Case089diagnosisFeedBack','Case089'),
                         # ('UICase.Case090diagnosisFeedBackNew', 'Case090'),
                         ('UICase.Case093checkdisagnosisHistory','Case093'),
                         ('UICase.Case094ShhuaweiKpiHvacCheck','Case094'),
                         ('UICase.Case095factorySearch','Case095'),
                         ('UICase.Case096MytestexportTime','Case096'),
                         ('UICase.Case097BatchAddCalcPoint','Case097'),
                         ('UICase.Case098AddDataSourceTitleDisappear','Case098'),
                         ('UICase.Case099checkguangmingReport','Case099'),
                         ('UICase.Case100checkGuangMingIndex','Case100'),
                         ('UICase.Case101checkEnergyScreen','Case101'),
                         ('UICase.Case102checkGuangMingHistoryPath','Case102'),
                         ('UICase.Case103dataStatistics','Case103'),
                         ('UICase.Case104calculationPointBatchHistory','Case104'),
                         ('UICase.Case105jingzhongEny','Case105'),
                         ('UICase.Case106jingzhongKPI','Case106'),
                         ('UICase.Case107jingzhongdoctor','Case107'),
                         ('UICase.Case108jingzhongdiag','Case108'),
                         ('UICase.Case109jingzhongreport','Case109'),
                         ('UICase.Case110checkfindpointfuntion','Case110'),
                         ('UICase.Case111rnbtechgrouppage','Case111'),
                        ]



class tester3(Base):
    pass



class tester5(Base):
    pass



class guangming(Base):
    pass

#配置集
user_conf = {
    'default':Base(),
    'kingsley':kingsley(),
    'sophia':sophia(),
    'woody':woody(),
    'angelia':angelia(),
    'tester1':tester1(),
    'tester2':tester2(),
    'tester3':tester3(),
    'tester5':tester5(),
    'guangming':guangming()
}

#默认配置
app.config.from_object(user_conf['default'])

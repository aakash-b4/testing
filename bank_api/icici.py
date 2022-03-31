# #IMPSliveurl
# url=https://api.icicibank.com:8443/api/Corporate/CAB/v1/InstaIMPSProcess

# #IMPSuaturl
# #url=https://apigwuat.icicibank.com:8443/api/Corporate/CAB/v1/InstaIMPSProcess/Test
#key=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCuZNbFjzwKJL8YLoIES3sIjLhDd52GaHfrOw73dB7Sc/i+ObVKHnsPbS7DWwPI5JNjseRmMvFSx0RgF8mljQTOwvfdlWTgSrKKUyAqqSkRVtYfbnIrYbgdiZdQ76ZTE1Fv43R/gRlwjb4YkKToDXBOibKXjmJciyE/1fA8d1eSfwIDAQAB
#key=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCuZNbFjzwKJL8YLoIES3sIjLhDd52GaHfrOw73dB7Sc/i+ObVKHnsPbS7DWwPI5JNjseRmMvFSx0RgF8mljQTOwvfdlWTgSrKKUyAqqSkRVtYfbnIrYbgdiZdQ76ZTE1Fv43R/gRlwjb4YkKToDXBOibKXjmJciyE/1fA8d1eSfwIDAQAB
#key=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDXOsNnHqH+gHozdSZIFgx2EDvEqNB/6dGHKzK5S4+aJtjtIeVWRlsMuq4Hle3hngPEBPFMrr7tgqRivPg9qm0XOO0niMphlxzZL3p49hZB3IDt0NC+O/4uiRYF6fU+SmTYGCwRFMAMutLrHCiRfFahRMBy7g1UWm0GHsh+uRKg9QIDAQAB
# key=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDXOsNnHqH+gHozdSZIFgx2EDvEqNB/6dGHKzK5S4+aJtjtIeVWRlsMuq4Hle3hngPEBPFMrr7tgqRivPg9qm0XOO0niMphlxzZL3p49hZB3IDt0NC+O/4uiRYF6fU+SmTYGCwRFMAMutLrHCiRfFahRMBy7g1UWm0GHsh+uRKg9QIDAQAB
#uatKey
#key=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCGG4+y8hy5p3hiUfjjHTt8YEhcqfFrt4OkWwYkiHlKBQrKp1cTAWk55bvFTQPo+YAxhIAlA0ymJ0FRuNOvgTUpg1QNoE8DKqscq+oCakF1cztRrVQYjQ3gLuzhdgpjJYsGuEFoqYaGfSN103hEc7Ur8QZr9YiWpKETMy88RR082wIDAQAB

#ICICI_IMPS Details
#iciciImpsUserName=SRSLIVET
#PassWord=SRSLIVET
# debitAccount=347505000468
# iciciImpsUserName=SRSLIVET
# PassWord=SRSLIVET
#CreditAccount=072101503207

def key():
    return "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDXOsNnHqH+gHozdSZIFgx2EDvEqNB/6dGHKzK5S4+aJtjtIeVWRlsMuq4Hle3hngPEBPFMrr7tgqRivPg9qm0XOO0niMphlxzZL3p49hZB3IDt0NC+O/4uiRYF6fU+SmTYGCwRFMAMutLrHCiRfFahRMBy7g1UWm0GHsh+uRKg9QIDAQAB"

def prod():
    return "https://api.icicibank.com:8443/api/Corporate/CAB/v1/InstaIMPSProcess"

def uat():
    return "https://apigwuat.icicibank.com:8443/api/Corporate/CAB/v1/InstaIMPSProcess/Test"

def icic_details():
    return {"iciciImpsUserName":"SRSLIVET","Password":"SRSLIVET","debitAccount":"347505000468"}
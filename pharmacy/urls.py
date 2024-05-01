from django.urls import path, include
from .import HODViews
from .import pharmacistViews,DoctorViews,views,patient_view,clerkViews
from django.contrib.auth import views as auth_views


urlpatterns=[
    path("ajax/", include("pharmacy.ajax.urls")),
    path('',HODViews.adminDashboard,name='admin_dashboard'),
    path('admin_user/patient_form/',HODViews.createPatient,name='patient_form'),
    path('admin_user/all_patients/',HODViews.allPatients,name='all_patients'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'), 
    # path('get_user_details/', views.get_user_details, name="get_user_details"),

    path('admin_user/add_pharmacist/',HODViews.createPharmacist,name='add_pharmacist'),
    path('admin_user/manage_pharmacist/',HODViews.managePharmacist,name='manage_pharmacist'),
    path('admin_user/add_doctor/',HODViews.createDoctor,name='add_doctor'),
    path('admin_user/manage_doctor/',HODViews.manageDoctor,name='manage_doctor'),
    path('admin_user/add_pharmacyClerk/',HODViews.createPharmacyClerk,name='add_pharmacyClerk'),
    path('admin_user/admin_user/manage_pharmacyClerk/',HODViews.managePharmacyClerk,name='manage_pharmacyClerk'),
    
    path('admin_user/add-medines-bulk-by-csv/',HODViews.upload_medicine_bulk_by_csv,name='upload_medicine_bulk_by_csv'),
    
    path('admin_user/add_stock/',HODViews.addStock,name='add_stock'),
    path('admin_user/manage_stock/',HODViews.manageStock,name='manage_stock'),  
    path('admin_user/manage-stock-expired/',HODViews.manageStockExpirerd, name='manage_stock_expired'), 
    path('admin_user/manage-inactive-stocks/',HODViews.manageStockPendingForApproval,name='manage_inactive_stock'), 
    path('admin_user/approve-inactive-stocks/<int:id>/',HODViews.approveMedicine,name='approve_inactive_stock'),   
    
    path('admin_user/add_category/',HODViews.addCategory,name='add_category'), 
    path('admin_user/manage_category/',HODViews.manageCategory,name='manage_category'), 
    path('admin_user/edit_category/<int:id>/',HODViews.editCategory,name='edit_category'), 
    path('admin_user/delete_category/<int:id>/',HODViews.deleteCategory,name='delete_category'), 
    
    # Hospital Item
    path('admin_user/add_hospital_item/',HODViews.addHospitalItem,name='add_hospital_item'), 
    path('admin_user/manage_hospital_item/',HODViews.manageHospitalItem,name='manage_hospital_item'), 
    path('admin_user/edit_hospital_item/<int:id>/',HODViews.editHospitalItem,name='edit_hospital_item'), 
    path('admin_user/delete_hospital_item/<int:id>/',HODViews.deleteHospitalItem,name='delete_hospital_item'), 
    
    
    path('admin_user/add_manufacturer/',HODViews.addManufacturer, name='add_manufacturer'), 
    path('admin_user/manage_manufacturer/',HODViews.manageManufacturer, name='manage_manufacturer'), 
    path('admin_user/edit_manufacturer/<int:id>/',HODViews.editManufacturer, name='edit_manufacturer'), 
    path('admin_user/delete_manufacturer/<int:id>/',HODViews.deleteManufacturer, name='delete_manufacturer'), 
    
    # Vender Views Urls
    path('admin_user/add_vender/',HODViews.addVender, name='add_vender'), 
    path('admin_user/manage_vender/',HODViews.manageVender, name='manage_vender'), 
    path('admin_user/edit_vender/<int:id>/',HODViews.editVender, name='edit_vender'), 
    path('admin_user/delete_vender/<int:id>/',HODViews.deleteVender, name='delete_vender'), 
    
    # Supplier Views Urls
    path('admin_user/add_supplier/',HODViews.addSupplier, name='add_supplier'), 
    path('admin_user/manage_supplier/',HODViews.manageSupplier, name='manage_supplier'), 
    path('admin_user/edit_supplier/<int:id>/',HODViews.editSupplier, name='edit_supplier'), 
    path('admin_user/delete_supplier/<int:id>/',HODViews.deleteSupplier, name='delete_supplier'), 
    
    
    path('admin_user/add_drug_type/',HODViews.addDrugType, name='add_drug_type'), 
    path('admin_user/manage_drug_type/',HODViews.manageDrugType, name='manage_drug_type'), 
    path('admin_user/edit_drug_type/<int:id>/',HODViews.editDrugType, name='edit_drug_type'), 
    path('admin_user/delete_drug_type/<int:id>/',HODViews.deleteDrugType, name='delete_drug_type'), 
    
    # Patient Addmission Urls
    path('admin_user/add_addmission/',HODViews.addAddmission, name='add_addmission'), 
    path('admin_user/manage_addmission/',HODViews.manageAddmission, name='manage_addmission'), 
    path('admin_user/edit_addmission/<int:id>/',HODViews.editAddmission, name='edit_addmission'), 
    path('admin_user/print_addmission/<int:id>/',HODViews.printAddmission, name='print_addmission'), 
    path('admin_user/delete_addmission/<int:id>/',HODViews.deleteAddmission, name='delete_addmission'), 
    
    # Department Urls
    path('admin_user/add_department/',HODViews.addDepartment, name='add_department'), 
    path('admin_user/manage_department/',HODViews.manageDepartment, name='manage_department'), 
    path('admin_user/edit_department/<int:id>/',HODViews.editDepartment, name='edit_department'), 
    path('admin_user/delete_department/<int:id>/',HODViews.deleteDepartment, name='delete_department'), 
    
    path('admin_user/add_drug_unit/',HODViews.addDrugUnit, name='add_drug_unit'), 
    path('admin_user/manage_drug_unit/',HODViews.manageDrugUnit, name='manage_drug_unit'), 
    path('admin_user/edit_drug_unit/<int:id>/',HODViews.editDrugUnit, name='edit_drug_unit'), 
    path('admin_user/delete_drug_unit/<int:id>/',HODViews.deleteDrugUnit, name='delete_drug_unit'), 
      
    path('admin_user/prescribe_drug/',HODViews.addPrescription,name='prescribe'),
    path('admin_user/edit_patient/<patient_id>/',HODViews.editPatient,name='edit_patient'),
    # path('add_patient_save/',HODViews.editPatientSave,name='edit_patient_save'),

    path('admin_user/delete_patient/<str:pk>/',HODViews.confirmDelete,name='delete_patient'),
    path('admin_user/patient_personalRecords/<pk>/',HODViews.patient_personalRecords,name='patient_record'),
    path('admin_user/delete_prescription/<str:pk>/',HODViews.deletePrescription,name='delete_prescription'),
    path('admin_user/doctor_profile/',DoctorViews.doctorProfile,name='doctor_profile'),
    path('admin_user/hod_profile/',HODViews.hodProfile,name='hod_profile'),
    path('admin_user/delete_doctor/<str:pk>/',HODViews.deleteDoctor,name='delete_doctor'),
    path('admin_user/delete_pharmacist/<str:pk>/',HODViews.deletePharmacist,name='delete_pharmacist'),
    path('admin_user/delete_receptionist/<str:pk>/',HODViews.deletePharmacyClerk,name='delete_clerk'),
    path('admin_user/hod_profile/editAdmin_profile/',HODViews.editAdmin,name='edit-admin'),
    path('admin_user/delete_drug/<str:pk>/',HODViews.deleteDrug,name='delete_drug'),


    path('admin_user/edit_pharmacist/<staff_id>/', HODViews.editPharmacist, name="edit_pharmacist"),
    path('admin_user/edit_doctor/<doctor_id>/', HODViews.editDoctor, name="edit_doctor"),
    path('admin_user/edit_receptionist/<clerk_id>/', HODViews.editPharmacyClerk, name="edit_clerk"),
    path('admin_user/edit_drug/<pk>/', HODViews.editStock, name="edit_drug"),
    path('admin_user/receive_drug/<pk>/', HODViews.receiveDrug, name="receive_drug"),
    path('admin_user/reorder_level/<str:pk>/', HODViews.reorder_level, name="reorder_level"),
    path('admin_user/drug_details/<str:pk>/', HODViews.drugDetails, name="drug_detail"),
    
    path('admin_user/pos/', HODViews.billingPOS, name="pos"),
    path('admin_user/pos/billing/<int:id>/print/', HODViews.billingPrintPOS, name="pos-billing-print"),
    path('admin_user/pos-billing-history/', HODViews.billingHistory, name="pos_billing_history"),
    
    path('admin_user/medicine-detailed-history/', HODViews.medicinesDetailView, name="medicine_details_history"),

    # parched invoice list
    path('admin_user/parched_invoice/', HODViews.purchased_invoice_list, name="parched_invoice_list"),
    path('admin_user/parched_invoice_detail/<int:pk>/', HODViews.purchased_invoice_detail, name="parched_invoice_detail"),

    path('patient_feedback_message/', pharmacistViews.patient_feedback_message, name="patient_feedback_message"),
    path('patient_feedback_message_reply/', pharmacistViews.patient_feedback_message_reply, name="patient_feedback_message_reply"),
    path('admin_user/delete_patient_feedback/<str:pk>/', pharmacistViews.deletefeedback, name="delete_fed"),

    path('delete_details/<str:pk>/', pharmacistViews.deleteDispense4, name="del_disp"),


    #Pharmacist
    path('pharmacist_home/',pharmacistViews.pharmacistHome,name='pharmacist_home'),
    path('pharmacist_manage_patients/',pharmacistViews.managePatientsPharmacist,name='manage_patient_pharmacist'),
    path('manage_disp/<pk>/',pharmacistViews.manageDispense,name='pharmacist_disp'),
    # path('manage_dispe/<str:pk>/',pharmacistViews.dispenseDrug,name='pharm_disp'),
    # path('manage_stock_form/<str:pk>/',pharmacistViews.dispense,name='pharm_disp2'),
    path('staff_profile/',pharmacistViews.userProfile,name='pharmacist_profile'),

    path('manage_stock2/',pharmacistViews.manageStock,name='manage_stock2'),   
    path('edit-stock2/<int:id>/',pharmacistViews.editStock,name='edit_stock2'),    
    path('manage_prescrip/',pharmacistViews.managePrescription,name='pharmacist_prescription'),
    path('pharmacist_user/drug_details/<str:pk>/', pharmacistViews.drugDetails, name="drug_detail2"),
    path('sell_slip/<str:pk>/', pharmacistViews.sell_slip, name="sell_slip"),
    path('view-invoice-slip/<int:pk>/', pharmacistViews.view_invoice_details, name="view_invoice"),
    path('pharmacist/patient_form/', pharmacistViews.createPatientPharmacist, name='patient_form3'),

    #Doctor
    path('doctor_home/',DoctorViews.doctorHome,name='doctor_home'),
    path('manage_patients/',DoctorViews.managePatients,name='manage_patient_doctor'),
    path('doctor_prescribe_drug/<str:pk>/',DoctorViews.addPrescription,name='doctor_prescribe2'),
    path('patient_personalDetails/<str:pk>/',DoctorViews.patient_personalDetails,name='patient_record_doctor'),
    path('manage_prescription_doctor/',DoctorViews.managePrescription,name='manage_precrip_doctor'),
    path('doctor_prescribe_delete/<str:pk>/',DoctorViews.deletePrescription,name='doctor_prescrip_delete'),
    path('doctor_prescribe_edit/<str:pk>/',DoctorViews.editPrescription,name='doctor_prescrip_edit'),

    #Patients
    path('patient_profile/',patient_view.patientProfile,name='patient_profile'),
    path('patient_home/',patient_view.patientHome,name='patient_home'),
    path('patient_feedback/',patient_view.patient_feedback,name='patient_feedback'),
    path('staff_feedback_save/', patient_view.patient_feedback_save, name="patient_feedback_save"),
    path('taken_home/',patient_view.patient_dispense3,name='taken_home'),
    path('delete_patient_feedback2/<str:pk>/',patient_view.Patientdeletefeedback, name="delete_fed2"),
    path('delete_dispen/',patient_view.myPrescriptionDelete,name='taken_delete'),

    #Receptionist
    path('receptionist_profile/',clerkViews.receptionistProfile,name='clerk_profile'),
    path('receptionist_home/',clerkViews.clerkHome,name='clerk_home'),
    path('receptionist/patient_form/',clerkViews.createPatient,name='patient_form2'),
    path('receptionist/all_patients/',clerkViews.allPatients,name='all_patients2'),
    path('receptionist/edit_patient/<patient_id>/',clerkViews.editPatient,name='edit_patient_clerk'),
    path('receptionist/patient_personalRecords/<str:pk>/',clerkViews.patient_personalRecords,name='patient_record_clerk'),
    path('receptionist/delete_patient/<str:pk>/',clerkViews.confirmDelete,name='delete_patient_clerk'),
    # path('receptionist/dispense_drug/<str:pk>/',pharmacistViews.dispenseDrug,name='dispense_drug'),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name="reset_password"),

    path('reset_password_sent/',auth_views.PasswordResetDoneView
    .as_view(template_name="password_reset_sent.html"),name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView
    .as_view(template_name="password_reset_form.html"),name="password_reset_confirm"),

    
   path('reset_password_complete/',auth_views.PasswordResetCompleteView
    .as_view(template_name="password_reset_done.html"),name="password_reset_complete"),

    # purchase url
    path("new-purchase/", HODViews.new_purchase_fun, name="new_purchase"),
    path("add-medicine-purchese/", HODViews.add_medicine_on_purchese_page, name="add_medicine_on_purchese_page"),
    path('search-stock/', HODViews.search_stock, name="search_stock"),
    path('add-search-stock/', HODViews.add_searched_stock, name="add_searched_stock"),
    path('delete-search-stock/<int:id>/', HODViews.delete_searched_stock, name="delete_searched_stock"),
    path('update-added-stock/', HODViews.update_added_stock_detail, name="update_added_stock_detail"),

    path("purchase-history/", HODViews.purchase_history, name="purchase_history"),

]

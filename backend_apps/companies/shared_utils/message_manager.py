languages = {
    "en",  # English
    "ar",  # Arabic
}
message = {
    "companies": {
        "check_name": {
            "required": {
                "en": "Company name is required.",
                "ar": "اسم الشركة مطلوب."
            },
            "min_length": {
                "en": "Company name must be at least 2 characters long.",
                "ar": "يجب أن يكون اسم الشركة على الأقل حرفين."
            },
            "max_length": {
                "en": "Company name must not exceed 255 characters.",
                "ar": "يجب ألا يتجاوز اسم الشركة 255 حرفًا."
            },
            "invalid_chars": {
                "en": "Company name contains invalid characters.",
                "ar": "اسم الشركة يحتوي على أحرف غير صالحة."
            },
            "duplicate": {
                "en": "A company with this name already exists.",
                "ar": "توجد شركة بهذا الاسم بالفعل."
            },
        },
        "check_is_active": {
            "required": {
                "en": "is_active field is required.",
                "ar": "حقل is_active مطلوب."
            },
            "invalid_type": {
                "en": "is_active must be a boolean value.",
                "ar": "يجب أن تكون قيمة is_active صحيحة أو خاطئة."
            },
        },
        "check_delete": {
            "related_objects_found": {
                "en": "Cannot delete: related objects exist.",
                "ar": "لا يمكن الحذف: توجد سجلات مرتبطة."
            },
            "deleted_successfully": {
                "en": "Company deleted successfully.",
                "ar": "تم حذف الشركة بنجاح."
            },
            "not_found": {
                "en": "Company not found.",
                "ar": "الشركة غير موجودة."
            },
        },
        "create_success": {
            "en": "Company created successfully.",
            "ar": "تم إنشاء الشركة بنجاح."
        },
        "update_success": {
            "en": "Company updated successfully.",
            "ar": "تم تحديث الشركة بنجاح."
        },
        "update_status_success": {
            "en": "Company status updated successfully.",
            "ar": "تم تحديث حالة الشركة بنجاح."
        },
        "view_success": {
            "en": "Company retrieved successfully.",
            "ar": "تم استرجاع الشركة بنجاح."
        },
        "all_success": {
            "en": "Companies retrieved successfully.",
            "ar": "تم استرجاع الشركات بنجاح."
        },
        "not_found": {
            "en": "Company not found.",
            "ar": "الشركة غير موجودة."
        },
    },
    "dashboard": {
        "stats_success": {
            "en": "Dashboard stats retrieved successfully.",
            "ar": "تم استرجاع إحصائيات لوحة التحكم بنجاح."
        },
    },
}
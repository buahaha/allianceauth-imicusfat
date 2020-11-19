# coding=utf-8

"""
creating a user permission hierarchy
"""


# checking permissions
def get_user_permissions(user):
    """
    checking the users permissions

    :param user:
    :return:
    """

    ##
    # defining the variables we need
    ##
    has_fatlink_permissions = False
    has_fat_permissions = False
    can_manage = False
    can_manipulate_fatlink = False
    can_add_fatlink = False
    can_change_fatlink = False
    can_delete_fatlink = False
    can_manipulate_fat = False
    can_add_fat = False
    can_delete_fat = False
    can_view_owncorpstats = False
    can_view_other_corpstats = False
    can_view_other_charstats = False

    ##
    # asigning them as we need to
    ##

    # can manage the fat module
    # meaning he can add, change and delete any fat or fatlink
    if user.has_perm("imicusfat.manage_imicusfat"):
        can_manage = True
        has_fatlink_permissions = True
        has_fat_permissions = True
        can_manipulate_fatlink = True
        can_add_fatlink = True
        can_change_fatlink = True
        can_delete_fatlink = True
        can_manipulate_fat = True
        can_add_fat = True
        can_delete_fat = True

    # check if the user has any permissions to manipulate fats and fatlinks
    if (
        user.has_perm("imicusfat.manage_imicusfat")  # has all permissions
        or user.has_perm("imicusfat.add_ifatlink")  # can add fatlinks
        or user.has_perm("imicusfat.change_ifatlink")  # can change fatlinks
        or user.has_perm("imicusfat.delete_ifatlink")  # can delete fatlinks
    ):
        has_fatlink_permissions = True
        can_manipulate_fatlink = True

    if (
        user.has_perm("imicusfat.manage_imicusfat")  # has all permissions
        or user.has_perm("imicusfat.add_ifat")  # can add fats
        or user.has_perm("imicusfat.delete_ifat")  # can delete fats
    ):
        has_fat_permissions = True
        can_manipulate_fat = True

    ##
    # Now let's check which permisions he has
    ##

    # can add fatlinks
    if user.has_perm("imicusfat.manage_imicusfat") or user.has_perm(
        "imicusfat.add_ifatlink"
    ):
        can_add_fatlink = True

    # Can change fatlinks
    if user.has_perm("imicusfat.change_ifatlink"):
        can_manipulate_fatlink = True
        can_change_fatlink = True

    # can delete fatlinks
    if user.has_perm("imicusfat.delete_ifatlink"):
        can_manipulate_fatlink = True
        can_delete_fatlink = True

    # can add fats
    if user.has_perm("imicusfat.add_ifat"):
        can_add_fat = True

    # can delete fats
    if user.has_perm("imicusfat.delete_ifat"):
        can_manipulate_fat = True
        can_delete_fat = True

    # can view other corp stats
    if user.has_perm("imicusfat.stats_corp_own"):
        can_view_owncorpstats = True

    # can view other corp stats
    if user.has_perm("imicusfat.stats_corp_other"):
        can_view_other_corpstats = True

    # can view other character stats
    if user.has_perm("imicusfat.stats_char_other"):
        can_view_other_charstats = True

    permissions = {
        "fatlinks": {
            "has_permissions": has_fatlink_permissions,  # has any of the below
            "manage": can_manage,  # has all of the below
            "add": can_add_fatlink,
            "manipulate": can_manipulate_fatlink,  # has any of the below
            "change": can_change_fatlink,
            "delete": can_delete_fatlink,
        },
        "fats": {
            "has_permissions": has_fat_permissions,  # has any of the below
            "manage": can_manage,  # has all of the below
            "add": can_add_fat,
            "manipulate": can_manipulate_fat,  # has any of the below
            "delete": can_delete_fat,
        },
        "stats": {
            "corp": {
                "view_own": can_view_owncorpstats,
                "view_other": can_view_other_corpstats,
            },
            "char": {"view_other": can_view_other_charstats},
        },
    }

    return permissions

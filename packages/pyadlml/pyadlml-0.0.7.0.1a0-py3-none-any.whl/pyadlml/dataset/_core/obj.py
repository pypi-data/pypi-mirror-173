from pyadlml.constants import DEVICE, ACTIVITY


class Data(object):
    def __init__(self, activities=None, devices=None, activity_list=None, device_list=None):

        self.df_devices = devices

        if device_list is None:
            self.lst_devices = devices[DEVICE].unique()

        if activities is not None:
            self.df_activities = activities
            if activity_list is None:
                self.lst_activities = activities[ACTIVITY].unique()
            else:
                self.lst_activities = activity_list
            self.act_dict = {"default": self.df_activities}
        else:
            self.act_dict = {}



    def set_activity_list(self, lst, name=None):
        """
        """
        if name is None or name == "default":
            setattr(self, "lst_activities", lst)
        else:
            setattr(self, "lst_activities_{}".format(name), lst)


    def set_activity_df(self, df, name=None):
        """
        """
        if name is None or name == "default":
            setattr(self, "df_activities", df)
            self.act_dict["default"] = df
        else:
            setattr(self, "df_activities_{}".format(name), df)
            self.act_dict[name] = df

    def set_activity_correction(self, lst, name=None):
        if name is None or name == "default":
            self.correction_activities = lst
        else:
            setattr(self, "correction_activities_{}".format(name), lst)

    def set_device_correction(self, corr_dts, corr_incons):
        self.correction_devices_duplicate_timestamps = corr_dts
        self.correction_devices_on_off_inconsistency = corr_incons

    def get_activity_dict(self) -> dict:
        return self.act_dict

    def set_device_df(self, df):
        self.df_devices = df
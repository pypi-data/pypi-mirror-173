""""
App Views.
"""
import logging
import json
from uuid import UUID
from aiohttp import web
from datetime import datetime
from dataclasses import asdict
from apps.worp.models import POTracker, tracker_defaults
from navigator.views import BaseHandler, BaseView, ModelView
from asyncdb.utils.encoders import BaseEncoder
from asyncpg.exceptions import UndefinedColumnError, UniqueViolationError
from asyncdb.exceptions import StatementError, NoDataFound


def is_valid_uid(test, version: int = 4):
    try:
        uuid_obj = UUID(test, version=version)
    except ValueError:
        return False
    except Exception as err:
        print(err)
        raise
    return str(uuid_obj) == test or uuid_obj.hex == test


class TrackerDefaults(BaseHandler):
    """
    Function utilities for managing PO Tracker Handlers.
    """
    async def get_defaults(self, request: web.Request, **kwargs):
        """get_defaults.

        description: returns the default values for PO Tracker.
        """
        headers = {
            'X-STATUS': 'OK',
            'X-MESSAGE': 'PO Tracker Defaults'
        }
        try:
            return self.json_response(
                response=asdict(
                    tracker_defaults
                ),
                headers=headers
            )
        except Exception as err:
            logging.exception(err)
            return self.error(
                request=request,
                exception=err,
                state=409
            )

    async def set_defaults(self, request: web.Request, **kwargs):
        """set_defaults.

        description: Change and returns the default values for PO Tracker.
        """
        headers = {
            'X-STATUS': 'OK',
            'X-MESSAGE': 'PO Tracker Defaults'
        }
        from __apps.worp.models import tracker_defaults as td
        data = await self.data(request=request)
        try:
            for key, val in data.items():
                if hasattr(td, key):
                    setattr(td, key, val)
        except Exception as err:
            logging.exception(err)
            return self.error(
                request=request,
                exception=err,
                state=409
            )
        return self.json_response(
            response=asdict(
                td
            ),
            headers=headers
        )

    async def get_values(self, request: web.Request, **kwargs):
        """set_defaults.

        description: Get PO Tracker calculated values.
        """
        headers = {
            'X-STATUS': 'OK',
            'X-MESSAGE': 'PO Tracker Values'
        }
        calculated = [
            "store_id", "po_number",
            "total_days",
            "merch_headcount", "lead_headcount", "team_capt_headcount",
            "total_headcount",
            "total_merchant_hours", "total_lead_hours",
            "total_capt_hours", "total_hours",
            "merch_billable_amount", "sup_billable_amount",
            "capt_billable_amount", "total_billable_amount",
            "merch_payable_amount", "sup_payable_amount",
            "capt_payable_amount",
            "total_payable_amount"
        ]
        data = await self.data(request=request)
        qs = self.get_arguments(request=request)
        if 'start_date' in data.keys():
            data['start_date'] = datetime.strptime(
                data['start_date'], '%Y-%m-%d').date()
        if 'end_date' in data.keys():
            data['end_date'] = datetime.strptime(
                data['end_date'], '%Y-%m-%d').date()
        if 'effective_date' in data.keys():
            data['effective_date'] = datetime.strptime(
                data['effective_date'], '%Y-%m-%d').date()
        if 'effective_end_date' in data.keys():
            data['effective_end_date'] = datetime.strptime(
                data['effective_end_date'], '%Y-%m-%d').date()
        try:
            tracker = POTracker(**data)
        except Exception as err:
            print(err)
            logging.exception(err)
            headers = {
                'X-STATUS': 'FAIL',
                'X-MESSAGE': 'Error: PO Tracker Calculation'
            }
            return self.error(
                request=request,
                response=f"WORP Error: {err!s}",
                exception=err,
                headers=headers,
                state=409
            )
        response = tracker.dict()
        try:
            del response['uid']
        except KeyError:
            pass
        if 'calculated' in qs.keys():
            try:
                tmp = {}
                for e in calculated:
                    tmp[e] = response[e]
                response = tmp
            except KeyError:
                pass
        return self.json_response(
            response=response,
            headers=headers,
            cls=BaseEncoder
        )

    async def get_trackers(self, request: web.Request, **kwargs):
        """get_trackers.

        description: Get PO Tracker calculated values.
        """
        qs = """
        select p.po_name, p.description, p.start_date, p.end_date, p.is_current, count(store_id) as num_trackers
        FROM worp.po_trackers p
        INNER JOIN worp.po_tracker USING(po_id)
        GROUP BY p.po_name, p.description, p.start_date, p.end_date, p.is_current
        """
        try:
            async with await request.app["database"].acquire() as db:
                result, error = await db.query(qs)
                if error:
                    raise Exception('No PO Trackers')
                trackers = [dict(row) for row in result]
                headers = {
                    'X-STATUS': 'OK',
                    'X-MESSAGE': 'PO Tracker List'
                }
                return self.json_response(
                    response=trackers,
                    headers=headers,
                    cls=BaseEncoder
                )
        except Exception as err:
            logging.exception(err)
            return self.error(
                exception=err,
                state=500
            )

    async def get_current(self, request: web.Request, **kwargs):
        """get_current.

        description: GET Current PO Tracker (based on po_id or po_name).
        """
        fields = """
            "po_id", "uid", "po_version", "po_name", "po_number",
            "store_id", "store_name", "market_id", "district_id", "region_id",
            "start_date", "end_date", "effective_date", "effective_end_date",
            "total_days", "project_days", "work_hours_per_day", "total_weeks",
            "hours_per_week", "adjusted_start_date", "adjusted_end_date",
            "adjusted_hours_per_week",
            "merch_headcount", "lead_headcount", "team_capt_headcount",
            "total_headcount",
            "total_merchant_hours", "total_lead_hours", "total_capt_hours",
            "total_hours",
            "billing_rate_merch", "billing_rate_sup", "billing_rate_capt",
            "merch_billable_amount", "sup_billable_amount",
            "capt_billable_amount", "total_billable_amount",
            "pay_rate_merch", "pay_rate_sup", "pay_rate_capt",
            "merch_payable_amount", "sup_payable_amount",
            "capt_payable_amount", "total_payable_amount", "po_billable_amount", "current_po"
        """
        qs = f"select {fields!s} FROM worp.vw_po_trackers WHERE is_current = true;"
        try:
            async with await request.app["database"].acquire() as db:
                result, error = await db.query(qs.format(fields=fields))
                if error:
                    raise Exception('No PO Trackers')
                trackers = [dict(row) for row in result]
                headers = {
                    'X-STATUS': 'OK',
                    'X-MESSAGE': 'PO Tracker Current'
                }
                return self.json_response(
                    response=trackers,
                    headers=headers,
                    cls=BaseEncoder
                )
        except Exception as err:
            logging.exception(err)
            return self.error(
                exception=err,
                state=500
            )


class Tracker(ModelView):
    model = POTracker

    async def get_connection(self):
        try:
            if not self.model.Meta.connection:
                db = await self.request.app["database"].acquire()
                self.model.Meta.connection = db
        except Exception as err:
            raise Exception(err)

    async def get(self):
        headers = {
            'X-STATUS': 'EMPTY',
            'X-MESSAGE': 'PO Tracker not Found'
        }
        try:
            await self.get_connection()
        except Exception as err:
            print(err)
            logging.exception(err)
            return self.error(
                exception=err,
                state=500
            )
        try:
            data = await self.data(
                request=self.request
            )
            qs = self.get_arguments()
            params = self.match_parameters()
            print(qs, params)
        except Exception as err:
            data = {}
            print(err)
        if 'uid' in params:
            """ Search only for a single Row (Store)."""
            try:
                tracker = await self.model.get(**params)
                if not tracker:
                    return self.no_content(headers=headers)
                if 'all_versions' in qs:
                    # get all existing version of a row
                    filter = {
                        "store_id": tracker.store_id,
                        "is_current": True
                        # "po_name": tracker.po_name
                    }
                    print('FILTER> ', filter)
                    trackers = await self.model.filter(**filter)
                    if not trackers:
                        return self.no_content(headers=headers)
                    # convert into list of trackers:
                    trackers = [t.dict() for t in trackers]
                    return self.json_response(
                        response=trackers,
                        headers=headers
                    )
                else:
                    # return existing row
                    return self.json_response(
                        response=tracker.dict(),
                        headers=headers
                    )
            except UndefinedColumnError as err:
                logging.exception(err)
                return self.error(
                    response=f'Invalid Column: {err!s}',
                    exception=err,
                    state=406
                )
            except Exception as err:
                print(err)
                logging.exception(err)
                return self.error(
                    exception=err,
                    state=500
                )
        else:
            not_current = False
            if 'not_current' in qs:
                not_current = True if qs['not_current'] == 'true' else False
            if not_current is True:
                # return the not current
                filter = {}
            else:
                filter = {
                    "is_current": True
                }
            if data:
                filter = {**filter, **data}

            try:
                trackers = await self.model.filter(**filter)
                if not trackers:
                    return self.no_content(headers=headers)
                # convert into list of trackers:
                trackers = [t.dict() for t in trackers]
                return self.json_response(
                    response=trackers,
                    headers=headers
                )
            except UndefinedColumnError as err:
                logging.exception(err)
                return self.error(
                    response=f'Invalid Column: {err!s}',
                    exception=err,
                    state=406
                )
            except Exception as err:
                logging.exception(err)
                return self.error(
                    exception=err,
                    state=500
                )

    async def patch(self):
        """
        patch.

        Update fields on existing row.
        """
        try:
            await self.get_connection()
        except Exception as err:
            print(err)
            logging.exception(err)
            return self.error(
                exception=err,
                state=500
            )
        headers = {
            'X-STATUS': 'PO TRACKER OK',
            'X-MESSAGE': 'PO Tracker Updated'
        }
        to_remove = (
            "start_date", "end_date"
        )
        try:
            data = await self.json_data()
            filter = self.match_parameters()
        except Exception as err:
            print(err)
        if 'uid' in filter:
            """ Update single PO Tracker."""
            try:
                uid = filter['uid']
                if is_valid_uid(uid):
                    filter = {
                        "uid": str(UUID(uid, version=4))
                    }
                else:
                    return self.error(
                        response=f'WORP: Invalid UUID Format: {filter!s}',
                        state=406
                    )
                tracker = await self.model.get(**filter)
                if not tracker:
                    headers = {
                        'X-STATUS': 'EMPTY',
                        'X-MESSAGE': 'PO Tracker not Found'
                    }
                    return self.no_content(headers=headers)
                # remove the conflict columns (start_date, end_date, etc)
                for e in to_remove:
                    try:
                        del data[e]
                    except KeyError:
                        pass
                await tracker.update_values(data)
                # change values, then, recalculate.
                tracker.recalculate()
                await tracker.save()
                headers = {
                    'X-STATUS': 'PO TRACKER OK',
                    'X-MESSAGE': 'PO Tracker Updated'
                }
                return self.json_response(
                    response=tracker.dict(),
                    headers=headers
                )
            except UndefinedColumnError as err:
                logging.exception(err)
                return self.error(
                    response=f'Invalid Column: {err!s}',
                    exception=err,
                    state=406
                )
            except Exception as err:
                logging.exception(err)
                return self.error(
                    exception=err,
                    state=500
                )
        else:
            # massive update of trackers.
            updated = []
            for elem in data:
                for e in to_remove:
                    try:
                        del elem[e]
                    except KeyError:
                        pass
                # get uid
                try:
                    id = elem['uid']
                    tracker = await self.model.get(uid=id)
                    if not tracker:
                        headers = {
                            'X-STATUS': 'EMPTY',
                            'X-MESSAGE': 'PO Tracker not Found'
                        }
                        return self.error(
                            response=f"Tracker: Missing UID {id}",
                            state=406
                        )
                    # updating values
                    await tracker.update_values(elem)
                    # change values, then, recalculate.
                    tracker.recalculate()
                    await tracker.save()
                    updated.append(tracker.dict())
                except UniqueViolationError as err:
                    return self.error(
                        f"Duplicated Error: {err!s}",
                        state=402
                    )
                except StatementError as err:
                    return self.error(
                        f"Contraint Error: {err!s}",
                        state=402
                    )
                except KeyError:
                    return self.error(
                        response="PO Tracker Record missing Key Column UID",
                        state=406
                    )
            # here
            headers = {
                'X-STATUS': 'PO TRACKER OK',
                'X-MESSAGE': 'PO Trackers List Updated'
            }
            return self.json_response(
                response=updated,
                headers=headers
            )

    async def put(self):
        """
        put.

        Creates a new PO Tracker.
        """
        try:
            await self.get_connection()
        except Exception as err:
            print(err)
            logging.exception(err)
            return self.error(
                exception=err,
                state=500
            )
        data = await self.json_data()
        filter = self.match_parameters()
        if 'uid' in filter:
            """
            Get an existing store and create a new Tracker.
            """
            uid = filter['uid']
            try:
                if is_valid_uid(uid):
                    filter = {
                        "uid": str(UUID(uid, version=4))
                    }
                    tracker = await self.model.get(**filter)
                else:
                    # get info about a current store
                    filter = {
                        "store_id": uid,
                        "is_current": True
                    }
                    trackers = await self.model.filter(**filter)
                    tracker = trackers.pop()
            except Exception as err:
                return self.error(
                    response={
                        "reason": "WORP: Invalid UUID Format",
                        "details": f"WORP UUID Error: Invalid UUID format: {err!s}"
                    },
                    state=406
                )
            try:
                # saving the old-one with new parameters:
                tracker.set_effective_date(data)
                await tracker.save()
                # update the current tracker
                try:
                    # check which is the greatest version for this store:
                    ft = {
                        "store_id": tracker.store_id
                    }
                    ver = await self.model.filter(**ft)
                    greatest = ver[0]
                    version = greatest.po_version
                except Exception as err:
                    print(err)
                    version = tracker.po_version
                tracker.po_version = version + 1
                print('VERSION ', tracker.po_version)
                tracker.effective_end_date = None
            except NoDataFound:
                tracker = None
            except Exception as err:
                logging.error(err)
                return self.error(
                    response={
                        "reason": "Can't save the current Tracker, Effective/End Date combination will conflict with previous Trackers. Hint: Please check the Effective Date of Previous Trackers.",
                        "details": f"WORP PO Tracker Error: {err!s}",
                    },
                    state=406
                    )
            if not tracker:
                # TODO: know the po_name of the current Tracker.
                # we can create an brand-new store-tracker.
                tracker = POTracker(**data)
            new_data = tracker.dict()
            try:
                del new_data['uid']
            except KeyError:
                pass
            # at now: create them.
            try:
                if data:
                    data = {**new_data, **data}
                    try:
                        del data['uid']
                        print(data)
                    except KeyError:
                        pass
                new_tracker = self.model(**data)
                result = await new_tracker.insert()
                if result:
                    tracker = await self.model.get(**result)
                headers = {
                    'X-STATUS': 'PO TRACKER OK',
                    'X-MESSAGE': 'PO Tracker INSERTED'
                }
                return self.json_response(
                    response=tracker.dict(),
                    headers=headers
                )
            except UniqueViolationError as err:
                return self.error(
                    response={
                        "reason": "WORP Duplicate error: already exists a PO Tracker with the same Start/Effective Date.",
                        "details": f"Duplicate Error: Already Exists an PO Tracker with the same Start/Effective Date: {err!s}",
                    },
                    state=402
                )
            except StatementError as err:
                if 'unq_worp_po_tracker_id' in str(err):
                    response = {
                        "reason": "Error: already exists a PO Tracker with the same version for this store, HINT: please select another version for duplicate.",
                        "details": f"WORP Duplicate Error: {err}"
                    }
                else:
                    response = {
                        "reason": "WORP Error: Error on Duplication, please see *Details* for more information.",
                        "details": f"WORP Duplicate Error: {err}"
                    }
                return self.error(
                    response=response,
                    state=402
                )
            except Exception as err:
                error = str(err)
                if 'unq_worp_po_tracker_id' in error:
                    response = {
                        "reason": "Error: already exists a PO Tracker with the same version for this store, HINT: please select another version for duplicate.",
                        "details": f"WORP Duplicate Error: {error}"
                    }
                elif 'unq_no_overlapping_effective_dates' in error:
                    response = {
                        "reason": "Error: Conflict existing Tracker, Effective Date overlaps a previous Tracker, HINT: please select an Effective Date that does not overlap any existing Tracker.",
                        "details": f"WORP Duplicate Error: {error}"
                    }
                else:
                    response = {
                        "reason": "WORP Error: Error on Duplication, please see *Details* for more information.",
                        "details": f"WORP Duplicate Error: {error}"
                    }
                return self.error(
                    response=response,
                    state=402
                )
                logging.error(err)
                return self.error(
                    response=response,
                    exception=err,
                    state=406
                )
        else:
            if not data:
                return self.error(
                    "We can't create a PO Tracker without arguments.",
                    state=401
                )
            try:
                id = data['id']
                del data['id']
            except KeyError:
                id = 1
            try:
                name = data['po_number']
                del data['po_number']
            except KeyError:
                name = 'A1111'
            try:
                start = data['start_date']
                del data['start_date']
            except KeyError:
                return self.error(
                    "Error: PO Tracker need an Start Date",
                    state=401
                )
            try:
                end = data['end_date']
                del data['end_date']
            except KeyError:
                return self.error(
                    "Error: PO Tracker need an End Date",
                    state=401
                )
            try:
                effective = data['effective_date']
                del data['effective_date']
            except KeyError:
                effective = 'null'
            attributes = {}
            defaults = {
                "hours_per_day": tracker_defaults.hours_per_day,
                "team_capt_headcount": tracker_defaults.team_capt_headcount,
                "billing_rate_merch": tracker_defaults.billing_rate_merch,
                "billing_rate_sup": tracker_defaults.billing_rate_sup,
                "billing_rate_capt": tracker_defaults.billing_rate_capt,
                "pay_rate_merch": tracker_defaults.pay_rate_merch,
                "pay_rate_sup": tracker_defaults.pay_rate_sup,
                "pay_rate_capt": tracker_defaults.pay_rate_capt,
                "special_travel_budget": tracker_defaults.special_travel_budget,
                "special_other_budget": tracker_defaults.special_other_budget,
                "addl_po_reqs": tracker_defaults.addl_po_reqs,
                "walmart_sup_billable_rate": tracker_defaults.walmart_sup_billable_rate,
            }
            if data:
                attributes = {**defaults, **data}
            attributes = json.dumps(attributes)
            sql = f"SELECT * FROM worp.po_tracker_create({name!r}, {id}, {start!r}, {end!r}, {effective}, '{attributes}'::jsonb);"
            try:
                async with await self.request.app["database"].acquire() as db:
                    row, error = await db.queryrow(sql)
                    if error:
                        raise Exception('No PO Tracker was created')
                    result = dict(row)
                    headers = {
                        'x-status': 'OK',
                        'x-message': 'PO Tracker Creation OK'
                    }
                    return self.json_response(
                        response=result,
                        headers=headers,
                        state=200
                    )
            except StatementError as err:
                error = str(err)
                headers = {
                    'x-status': 'Error',
                    'x-message': 'Faild Creation: PO Tracker'
                }
                if 'unq_no_overlapping_effective_dates' in error:
                    response = {
                        "response": {
                            "reason": f"Current Tracker has conflicting Effective Date with another Tracker",
                            "details": f"Current Tracker has conflict with existing Tracker: {error!s}",
                        },
                        "headers": headers,
                        "state": 406
                    }
                if 'unq_no_overlapping_range_dates' in error:
                    response = {
                        "response": {
                            "reason": f"Current Tracker has conflict with other existing Tracker",
                            "details": f"Current Tracker has conflict with existing Tracker: {error!s}",
                        },
                        "headers": headers,
                        "state": 406
                    }
                elif 'range lower' in error:
                    response = {
                        "response": {
                            "reason": "WORP Tracker Error: END DATE need to be greater than START DATE",
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "state": 406
                    }
                elif 'overflow' in error:
                    response = {
                        "response": {
                            "reason": f"TRACKER Overflow: Some values in Pay/Billing Rates are greater than expected values: {error!s}",
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "state": 409
                    }
                elif 'po_tracker_check' in error:
                    response = {
                        "response": {
                            "reason": "TRACKER Error: EFFECTIVE DATE need to be greater than START DATE",
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "state": 409
                    }
                else:
                    response = {
                        "response": {
                            "reason": error,
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "state": 403
                    }
                return self.error(
                    **response
                )
            except Exception as err:
                headers = {
                    'x-status': 'Empty',
                    'x-message': 'Missing PO Tracker'
                }
                return self.error(
                    exception=err,
                    headers=headers,
                    state=404
                )

    async def delete(self):
        """
        delete.

        remove the fields on existing row.
        TODO: Check after delete if a previous version exists and enabled.
        """
        try:
            await self.get_connection()
        except Exception as err:
            print(err)
            logging.exception(err)
            return self.error(
                exception=err,
                state=500
            )
        try:
            # data = await self.post_data()
            filter = self.match_parameters()
        except Exception as err:
            print(err)
        if 'uid' in filter:
            try:
                tracker = await self.model.get(**filter)
                if tracker:
                    state = await tracker.delete()
                    headers = {
                        'x-status': 'OK',
                        'x-message': 'PO Tracker DELETED OK'
                    }
                    result = {
                        "message": state,
                        "filter": filter
                    }
                    return self.json_response(
                        response=result,
                        headers=headers,
                        state=201
                    )
            except NoDataFound:
                result = {
                    "message": "DELETE 0",
                    "filter": filter
                }
                headers = {
                    'x-status': 'NOT FOUND',
                    'x-message': 'PO Tracker DELETED NOT FOUND'
                }
                return self.json_response(
                    response=result,
                    headers=headers,
                    state=404
                )
            except Exception as err:
                logging.exception(err)

    async def post(self):
        try:
            await self.get_connection()
        except Exception as err:
            print(err)
            logging.exception(err)
            return self.error(
                exception=err,
                state=500
            )
        rem = ['inserted_at', 'updated_at', 'modified_by', 'created_by']
        try:
            data = await self.json_data()
            filter = self.match_parameters()
        except Exception as err:
            print(err)
        if 'uid' in filter:
            """ Update only a single Store."""
            try:
                uid = filter['uid']
                if is_valid_uid(uid):
                    filter = {
                        "uid": str(UUID(uid, version=4))
                    }
                else:
                    raise Exception(
                        f"WORP: Wrong format on Tracker UUID: {uid}"
                    )
                tracker = await self.model.get(**filter)
                old_effective = tracker.effective_date
                for k in rem:
                    try:
                        del data[k]
                    except KeyError:
                        pass
                if 'effective_date' in data.keys():
                    # I will change the effective date
                    try:
                        eff = datetime.strptime(
                            data['effective_date'], "%Y-%m-%d"
                        ).date()
                    except Exception as err:
                        raise Exception(
                            f'WORP: Wrong format in Effective Date: {err!s}'
                        )
                    if eff != old_effective:
                        logging.debug('Creating a new Tracker')
                        # I need to create a new one
                        tracker.set_effective_date(data)
                        await tracker.save()
                        tracker.po_version += 1
                        tracker.effective_end_date = None
                        await tracker.update_values(data)
                        tracker.recalculate()
                        new_data = tracker.dict()
                        try:
                            del new_data['uid']
                        except KeyError:
                            pass
                        new_tracker = self.model(**new_data)
                        result = await new_tracker.insert()
                        if result:
                            tracker = await self.model.get(**result)
                    else:
                        await tracker.update_values(data)
                        # change values, then, recalculate.
                        tracker.recalculate()
                        # saving the existing
                        await tracker.save()
                else:
                    await tracker.update_values(data)
                    # change values, then, recalculate.
                    tracker.recalculate()
                    # saving the existing
                    await tracker.save()
                headers = {
                    'X-STATUS': 'PO TRACKER OK',
                    'X-MESSAGE': 'PO Trackers List Updated'
                }
                return self.json_response(
                    response=tracker.dict(),
                    headers=headers
                )
            except UniqueViolationError as err:
                return self.error(
                    f"Duplicated Error: {err!s}",
                    state=402
                )
            except StatementError as err:
                return self.error(
                    f"Contraint Error: {err!s}",
                    state=402
                )
            except Exception as err:
                error = str(err)
                logging.error(err)
                headers = {
                    'x-status': 'Error',
                    'x-message': 'WORP PO Tracker: Updated Failed.'
                }
                if 'unq_no_overlapping_effective_dates' in error:
                    response = {
                        "response": {
                            "reason": f"Current Tracker has conflicting Effective Date with another Tracker",
                            "details": f"Current Tracker has conflict with existing Tracker: {error!s}",
                        },
                        "headers": headers,
                        "state": 406
                    }
                elif 'unq_no_overlapping_range_dates' in error:
                    response = {
                        "response": {
                            "reason": f"Current Tracker has conflict with other existing Tracker",
                            "details": f"Current Tracker has conflict with existing Tracker: {error!s}",
                        },
                        "headers": headers,
                        "state": 406
                    }
                elif 'range lower' in error:
                    response = {
                        "response": {
                            "reason": "WORP Tracker Error: END DATE need to be greater than START DATE",
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "state": 406
                    }
                elif 'overflow' in error:
                    response = {
                        "response": {
                            "reason": f"TRACKER Overflow: Some values in Pay/Billing Rates are greater than expected values: {error!s}",
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "state": 409
                    }
                elif 'po_tracker_check' in error:
                    response = {
                        "response": {
                            "reason": "TRACKER Error: EFFECTIVE DATE need to be greater than START DATE",
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "state": 409
                    }
                else:
                    response = {
                        "response": {
                            "reason": error,
                            "details": f"WORP Tracker Error: {err}",
                        },
                        "headers": headers,
                        "state": 403
                    }
                return self.error(
                    **response
                )

    class Meta:
        tablename: str = 'po_tracker'
        schema: str = 'worp'


class PO_Tracker(BaseView):
    """
    Walmart Overnight PO Tracker.

    Managing the PO Tracker instance, create, reset, delete or update the PO Tracker.
    """

    async def get(self):
        """
        GET Method.
        description: get all current PO Trackers, all versions or a simple Tracker by ID or Store ID.
        tags:
        - po tracker
        consumes:
        - application/json
        produces:
        - application/json
        responses:
            "200":
                description: Existing PO Tracker was retrieved.
            "403":
                description: Forbidden Call
            "404":
                description: No PO Trackers(s) were found
            "406":
                description: Query Error
        """
        headers = {
            'X-STATUS': 'EMPTY',
            'X-MESSAGE': 'PO Tracker not Found'
        }
        return self.no_content(headers=headers)

    async def post(self):
        """
        POST Method.
        description: inserting or updating a PO Tracker by Store ID (or bulk)
        tags:
        - po tracker
        - Database connections
        consumes:
        - application/json
        produces:
        - application/json
        responses:
            "200":
                description: Existing PO Tracker was updated.
            "201":
                description: a New PO Tracker was inserted
            "202":
                description: a new version of PO Tracker were added.
            "400":
                description: Failed to execute
            "403":
                description: Forbidden Call
            "404":
                description: No PO Trackers were found
            "406":
                description: Query Error
            "409":
                description: Conflict, a constraint was violated
        """
        headers = {
            'X-STATUS': 'EMPTY',
            'X-MESSAGE': 'PO Tracker not Found'
        }
        return self.no_content(headers=headers)

    async def put(self):
        """
        PUT Method.
        description: creating a entirely new PO Tracker.
        tags:
        - PO Tracker
        - Bulk Creation PO Tracker
        - Database connections
        produces:
        - application/json
        consumes:
        - application/merge-patch+json
        - application/json
        responses:
            "200":
                description: An existing PO Tracker exists.
            "201":
                description: New PO Tracker was inserted
            "400":
                description: Invalid resource according data schema
            "403":
                description: Forbidden Call
            "404":
                description: No Data was found
            "406":
                description: Query Error
            "409":
                description: Conflict, a constraint was violated
        """
        headers = {
            'X-STATUS': 'EMPTY',
            'X-MESSAGE': 'PO Tracker not Found'
        }
        return self.no_content(headers=headers)

    async def delete(self):
        """
        delete Method.
        description: Deleting a PO Tracker.
        tags:
        - PO Tracker
        produces:
        - application/json
        consumes:
        - application/json
        responses:
            "200":
                description: Existing PO Tracker by ID or Store was Deleted.
            "203":
                description: A list of PO Trackers were accepted for deleted.
            "400":
                description: Invalid resource according data schema
            "403":
                description: Forbidden Call
            "404":
                description: No Data was found
            "406":
                description: Query Error
            "409":
                description: Conflict, a constraint was violated
        """
        headers = {
            'X-STATUS': 'EMPTY',
            'X-MESSAGE': 'PO Tracker not Found'
        }
        return self.no_content(headers=headers)

    async def patch(self):
        """
        PATCH Method.
        description: updating partially info about a PO Tracker
        tags:
        - PO Tracker
        consumes:
        - application/merge-patch+json
        produces:
        - application/json
        responses:
            "200":
                description: Existing PO Tracker was updated.
            "201":
                description: a New PO Tracker was inserted (with default values)
            "304":
                description: PO Tracker not modified, its currently the actual version
            "403":
                description: Forbidden Call
            "404":
                description: No Data was found
            "406":
                description: Query Error
            "409":
                description: Conflict, a constraint was violated
        """
        headers = {
            'X-STATUS': 'EMPTY',
            'X-MESSAGE': 'PO Tracker not Found'
        }
        return self.no_content(headers=headers)

import logging
from aiohttp import web
from navigator.views import DataView
from resources.helper import Compile, Tools
from navigator_session import get_session

class ModulesServices(DataView):

    async def get(self):
        """
        ---
        description: Get all user modules on the client
        tags:
        - ModulesServices
        produces:
        - application/json
        parameters:
        - name: sessionid
          description: session of Django
          in: headers
          required: true
          type: string
        responses:
            "200":
                description: returns valid data
            "204":
                description: No data
            "403":
                description: Forbidden Call
        """
        try:
            try:
                session = await get_session(self.request)
                session = session['session']
                # print('SESSION: ', session)
            except KeyError:
                session = None
            print('GROUPS ', session, type(session))
            try:
                employee_group = [x for x in session['groups']]
            except (KeyError, TypeError):
                employee_group = None
            print(employee_group)
            try:
                client = self.request.get('client')
            except KeyError:
                client = None

            result = None
            if session and employee_group:
                sql = f"select  module_id, module_name, allow_filtering, filtering_show, module_slug, conditions, \
                module_description as description, module_attributes as attributes, program_id, \
                parent_module_id, group_id, group_name from troc.vw_group_modules \
                where client_slug = {client!r} AND group_name = ANY(ARRAY{employee_group!r}) \
                group by module_id, module_name, allow_filtering, filtering_show,conditions, \
                module_slug,  module_description, module_attributes, program_id, parent_module_id, group_id, group_name "
                print('SQL: ', sql)
                await self.connect(self.request)
                try:
                    result = await self.query(sql)
                except Exception as err:
                    logging.error(f'Error on Module Service: {err!s}')
                    result = None
            if result:
                modules_list = [dict(row) for row in result]
                headers = {
                    'x-status': 'OK',
                    'x-message': 'Module List OK'
                }
                return self.json_response(
                    response=modules_list,
                    headers=headers,
                    state=200
                )
            else:
                headers = {
                    'x-status': 'Empty',
                    'x-message': 'Module information not found'
                }
                return self.no_content(headers=headers)
        except Exception as e:
            print(e)
            return self.critical(self.request, e)
        finally:
            await self.close()

    async def post(self):
        """
        post.
           TODO write doc
        """
        try:
            await self.connect(self.request)
            content = await self.json_data(self.request)
            try:
                session = await get_session(self.request)
                session = session['session']
            except (KeyError, TypeError):
                session = None

            if 'superuser' not in session['groups']:
                headers = {
                    'x-status': 'FAILED',
                    'x-message': 'Forbidden'
                }
                data = {'message':'Forbidden'}
                code = 403

                return self.json_response(
                    response=data,
                    headers=headers,
                    state=code
                    )

            if content:
                required = ["program_slug","client_slug","client_id"]

                try:
                    dashboard_id = content['dashboard_id']
                except KeyError:
                    dashboard_id = None
                    if 'dashboard_id' in required:
                        return Tools.validate(self,'dashboard_id')
                try:
                    module_id = content['module_id']
                except KeyError:
                    module_id = None
                    if 'module_id' in required:
                        return Tools.validate(self,'module_id')

                if module_id is None:
                    try:
                        module = content['module']
                    except KeyError:
                        module = None
                    if 'module' in required:
                        return Tools.validate(self,'module')

                    try:
                        module_id = module['module_id']
                    except KeyError:
                        module_id = None
                        if 'module_id' in required:
                            return Tools.validate(self,'module_id')

                    try:
                        program_slug = content['program_slug']
                    except KeyError:
                        program_slug = None
                        if 'program_slug' in required:
                            return Tools.validate(self,'program_slug')

                    try:
                        client_slug = content['client_slug']
                    except KeyError:
                        client_slug = None
                        if 'client_slug' in required:
                            return Tools.validate(self,'client_slug')

                    try:
                        client_id = content['client_id']
                    except KeyError:
                        client_id = None
                        if 'client_id' in required:
                            return Tools.validate(self,'client_id')

                if module_id is None:
                    result = None
                    if module is not None:
                        ## insert new module
                        sqlModule =  Compile.insert('troc.troc_modules', module, 'module_id')
                        result = await self.queryrow(sqlModule)
                        module_id = result["module_id"]

                        ## insert relation module with client
                        sqlClient =  Compile.insert('troc.troc_client_modules',{"client_id":client_id,"program_id":module["program_id"],"module_id":module_id,"client_slug":client_slug,"program_slug":program_slug,"module_slug":module["module_slug"],"active":True})
                        await self.execute(sqlClient)

                        ## insert relation module with group
                        sqlGroup =  Compile.insert('troc.troc_modules_group',{"groups_id":1,"module_id":module_id})
                        await self.execute(sqlGroup)

                    if dashboard_id is not None and module_id is not None:
                        ## update dashboard
                        sqlUpdateDashboard = Compile.update('troc.dashboards', {"user_id":"null","module_id":module_id}, {"dashboard_id":dashboard_id})
                        await self.execute(sqlUpdateDashboard)

                    if result is not None:
                        headers = {
                            'x-status': 'OK',
                            'x-message': 'Registered module'
                        }
                        data = {'message':'registered module'}
                        code = 200
                    else:
                        headers = {
                            'x-status': 'ERROR',
                            'x-message': 'An error has occurred'
                        }
                        data = {'message':'An error has occurred'}
                        code = 500

                elif module_id is not None and dashboard_id is not None:
                    ## update dashboard
                    sqlUpdateDashboard = Compile.update('troc.dashboards', {"user_id":"null","module_id":module_id}, {"dashboard_id":dashboard_id})
                    await self.execute(sqlUpdateDashboard)

                    headers = {
                        'x-status': 'OK',
                        'x-message': 'Update module in dashboard'
                    }
                    data = {'message':'Update module in dashboard'}
                    code = 200

                else:
                    headers = {
                    'x-status': 'FAILED',
                    'x-message': 'Bad Request'
                    }
                    data ={'message':'Bad Request'}
                    code = 400

            else:
                headers = {
                    'x-status': 'FAILED',
                    'x-message': 'Bad Request'
                }
                data ={'message':'Bad Request'}
                code = 400

            return self.json_response(
                    response=data,
                    headers=headers,
                    state=code
                    )
        except Exception as e:
            print(e)
            return self.critical(self.request, e)
        finally:
            await self.close()

    async def put(self):
        """
        put.
           TODO write doc
        """
        try:
            await self.connect(self.request)
            content = await self.json_data(self.request)
            try:
                session = await get_session(self.request)
                session = session['session']
            except (KeyError, TypeError):
                session = None

            if 'superuser' not in session['groups']:
                headers = {
                    'x-status': 'FAILED',
                    'x-message': 'Forbidden'
                }
                data = {'message':'Forbidden'}
                code = 403

                return self.json_response(
                    response=data,
                    headers=headers,
                    state=code
                    )

            if content:
                required = ["module","program_slug","client_slug","client_id","program_slug","group_id"]
                try:
                    module = content['module']
                except KeyError:
                    module = None
                    if 'module' in required:
                        return Tools.validate(self,'module')
                try:
                    program_slug = content['program_slug']
                except KeyError:
                    program_slug = None
                try:
                    clients_slug = content['clients_slug']
                except KeyError:
                    clients_slug = None
                try:
                    clients_id = content['clients_id']
                except KeyError:
                    clients_id = None

                try:
                    groups = content['groups']
                except KeyError:
                    groups = None
                try:
                    if content['module_id'] is not None:
                        module_id = content['module_id']
                    else:
                        module_id = module['module_id']
                except KeyError:
                    module_id = None

                if module_id is not None:
                    if module is not None:
                        ## update module
                        sqlModule =  Compile.update('troc.troc_modules', module, {"module_id":module_id},'*')
                        result = await self.queryrow(sqlModule)

                    if groups is not None and isinstance(groups, list):
                        ## update groups
                        sqlDeleteGroup = Compile.delete('troc.troc_modules_group',{"module_id":module_id})
                        await self.execute(sqlDeleteGroup)
                        for group_id in groups:
                            sqlGroup =  Compile.insert('troc.troc_modules_group',{"groups_id":group_id,"module_id":module_id})
                            await self.execute(sqlGroup)
                    if result and program_slug and clients_id is not None and isinstance(clients_id, list) and clients_slug and isinstance(clients_slug, list):
                        ## update relation module with groups
                        sqlDeleteClientModule = Compile.delete('troc.troc_client_modules',{"module_id":module_id})
                        await self.execute(sqlDeleteClientModule)
                        for index, client_id in enumerate(clients_id):
                            ## update relation module with client
                            sqlClient =  Compile.insert('troc.troc_client_modules',{"client_id":client_id,"program_id":result["program_id"],"module_id":module_id,"client_slug":clients_slug[index],"program_slug":program_slug,"module_slug":result["module_slug"],"active":result['active']})
                            await self.execute(sqlClient)


                    headers = {
                        'x-status': 'OK',
                        'x-message': 'Update module'
                        }
                    data = {'message':'update module'}
                    code = 200
                else:
                    headers = {
                    'x-status': 'FAILED',
                    'x-message': 'Bad Request'
                    }
                    data ={'message':'Bad Request'}
                    code = 400
            else:
                headers = {
                    'x-status': 'FAILED',
                    'x-message': 'Bad Request'
                }
                data ={'message':'Bad Request'}
                code = 400

            return self.json_response(
                    response=data,
                    headers=headers,
                    state=code
                    )

        except Exception as e:
            print(e)
            return self.critical(self.request, e)
        finally:
            await self.close()

    async def delete(self):
        try:
            await self.connect(self.request)
            content = await self.json_data(self.request)
            try:
                session = await get_session(self.request)
                session = session['session']
            except (KeyError, TypeError):
                session = None

            if 'superuser' not in session['groups']:
                headers = {
                    'x-status': 'FAILED',
                    'x-message': 'Forbidden'
                }
                data = {'message':'Forbidden'}
                code = 403

                return self.json_response(
                    response=data,
                    headers=headers,
                    state=code
                    )
            if content:
                required = ["module_id"]

                try:
                    module_id = content['module_id']
                except KeyError:
                    module_id = None
                    if 'module_id' in required:
                        return Tools.validate(self,'module_id')

                if module_id is not None:
                    ## delete module
                    sqlDeleteModuleClient = Compile.update('troc.troc_client_modules', {"active":"false"}, {"module_id":module_id})
                    await self.execute(sqlDeleteModuleClient)

                    sqlDeleteModule = Compile.update('troc.troc_modules', {"active":"false"}, {"module_id":module_id})
                    await self.execute(sqlDeleteModule)

                    headers = {
                        'x-status': 'OK',
                        'x-message': 'Deleted module'
                    }
                    data = {'message':'Deleted module'}
                    code = 200

                else:
                    headers = {
                    'x-status': 'FAILED',
                    'x-message': 'Bad Request'
                    }
                    data ={'message':'Bad Request'}
                    code = 400

            else:
                headers = {
                    'x-status': 'FAILED',
                    'x-message': 'Bad Request'
                }
                data ={'message':'Bad Request'}
                code = 400

            return self.json_response(
                    response=data,
                    headers=headers,
                    state=code
                    )
        except Exception as e:
            print(e)
            return self.critical(self.request, e)
        finally:
            await self.close()

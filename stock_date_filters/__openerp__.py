# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Marc Cassuto (marc.cassuto@gmail.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Date filters in stock moves',
    'version': '0.1',
    'author': 'Marc Cassuto <marc.cassuto@gmail.com>',
    'license': 'AGPL-3',
    'category': 'Stock',
    'summary': 'Adds date filters to the stock_move search view',
    'description': """
This module adds 3 pre-defined filters into the stock move search view :

* Previous day
* Previous week
* Previous month

Contributors
-------------
* Marc Cassuto (marc.cassuto@gmail.com)
* Vincent Vinet (vincent.vinet@savoirfairelinux.com)
""",
    'depends': [
        'stock',
        'web_relativedelta',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'stock_move_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}

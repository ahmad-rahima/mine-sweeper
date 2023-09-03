pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'mine_sweeper')
gnome = import('gnome')

gnome.compile_resources('mine-sweeper',
  'mine-sweeper.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'mine-sweeper.in',
  output: 'mine-sweeper',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

mine_sweeper_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'main_content.py',
  'cell.py',
  'status_bar.py',
]

install_data(mine_sweeper_sources, install_dir: moduledir)
